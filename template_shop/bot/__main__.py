import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from arq import create_pool

from template_shop.bot.dialogs import register_dialogs
from template_shop.bot.handlers import register_handlers
from template_shop.bot.middlewares.db import DBSessionMiddleware
from template_shop.bot.middlewares.locale import LocaleMiddleware
from template_shop.bot.services.locale import Localizator, configure_localizator
from template_shop.bot.services.tg_helpers import send_tg_message
from template_shop.core.config import Settings
from template_shop.core.constants import LOCALES_FOLDER
from template_shop.core.logger import configure_logging
from template_shop.core.payment_clients.aiocryptopay import AioCryptoPay
from template_shop.infrastructure.config_loader import load_config
from template_shop.infrastructure.database.main import build_sa_engine, build_sa_session_factory

logger = logging.getLogger(__name__)


def setup_middlewares(
    dp: Dispatcher,
    session_factory,
    localizator: Localizator,
):
    dp.callback_query.outer_middleware(DBSessionMiddleware(session_factory))
    dp.update.outer_middleware(DBSessionMiddleware(session_factory))
    dp.message.outer_middleware.register(LocaleMiddleware(localizator))
    dp.errors.outer_middleware.register(LocaleMiddleware(localizator))
    dp.update.outer_middleware(LocaleMiddleware(localizator))
    dp.callback_query.outer_middleware.register(LocaleMiddleware(localizator))


async def main():
    config = load_config(Settings)
    configure_logging()

    logger.error("Starting bot")

    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(
            url=config.redis.url,
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    engine = build_sa_engine(config.db)
    session_factory = build_sa_session_factory(engine)
    localizator = configure_localizator(LOCALES_FOLDER)
    aiocryptopay = AioCryptoPay(token=config.payment.crypto_token)
    redis_pool = await create_pool(config.redis.pool_settings)

    setup_middlewares(dp, session_factory, localizator)

    setup_dialogs(dp)
    register_handlers(dp, config)
    register_dialogs(dp)

    await send_tg_message(bot, config.tg_bot.developer_id, "Бот запущен!")
    try:
        await dp.start_polling(
            bot,
            aiocryptopay=aiocryptopay,
            arqredis=redis_pool,
            config=config,
        )
    finally:
        await bot.session.close()
        await engine.dispose()
        logger.info("Bot stopped")


def cli():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == "__main__":
    cli()
