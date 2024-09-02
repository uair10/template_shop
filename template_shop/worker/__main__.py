import asyncio
import contextlib
import logging
from typing import Any

import pytz
from aiogram import Bot
from arq import cron
from arq.worker import create_worker

from template_shop.bot.services.locale import configure_localizator
from template_shop.core.config import RedisConfig, Settings
from template_shop.core.constants import LOCALES_FOLDER
from template_shop.core.logger import configure_logging
from template_shop.core.payment_clients.aiocryptopay import AioCryptoPay
from template_shop.infrastructure.config_loader import load_config
from template_shop.infrastructure.database.main import build_sa_engine, build_sa_session_factory
from template_shop.infrastructure.database.services.bill import BillService
from template_shop.infrastructure.database.services.bot_settings import BotSettingsService
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.user import UserService
from template_shop.infrastructure.database.uow.uow import build_uow
from template_shop.worker.jobs import check_bills, notify_users

logger = logging.getLogger(__name__)


async def startup(ctx):
    config = load_config(Settings)
    configure_logging()
    engine = build_sa_engine(config.db)
    ctx["engine"] = engine
    ctx["sessionmaker"] = build_sa_session_factory(engine)
    ctx["config"] = config
    ctx["bot"] = Bot(token=config.tg_bot.token, parse_mode="HTML")
    ctx["fluent"] = configure_localizator(LOCALES_FOLDER)
    ctx["aiocryptopay"] = AioCryptoPay(token=config.payment.crypto_token)


async def shutdown(ctx):
    if ctx.get("session"):
        await ctx["session"].close()
    await ctx["bot"].session.close()
    await ctx["engine"].dispose()


async def on_job_start(ctx):
    """Прокидываем зависимости в задачу"""

    session = ctx["sessionmaker"]()
    uow = build_uow(session)
    ctx["session"] = session
    ctx["uow"] = uow
    ctx["user_service"] = UserService(uow=uow)
    ctx["order_service"] = OrderService(uow=uow)
    ctx["bill_service"] = BillService(uow=uow)
    ctx["bot_settings_service"] = BotSettingsService(uow=uow)


async def after_job_end(ctx):
    await ctx["session"].close()


def create_worker_settings(redis_config: RedisConfig) -> dict[str, Any]:
    return {
        "functions": [
            notify_users,
            check_bills,
        ],
        "on_startup": startup,
        "on_shutdown": shutdown,
        "on_job_start": on_job_start,
        "after_job_end": after_job_end,
        "timezone": pytz.timezone("Europe/Moscow"),
        "allow_abort_jobs": True,
        "redis_settings": redis_config.pool_settings,
        "cron_jobs": [
            cron(check_bills, microsecond=0, max_tries=2),
        ],
    }


async def main():
    configure_logging()
    config = load_config(RedisConfig, "redis")

    worker_settings = create_worker_settings(config)
    worker = create_worker(worker_settings)

    try:
        logger.info("Starting worker")
        await worker.async_run()
    finally:
        logger.info("Worker stopped")
        await worker.close()


if __name__ == "__main__":
    with contextlib.suppress(asyncio.CancelledError):
        asyncio.run(main())
