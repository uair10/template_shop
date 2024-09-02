import logging
from datetime import date, datetime
from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from arq import ArqRedis

from template_shop.bot.states.admin import MailingSG
from template_shop.core.utils.date_time import get_date_time

logger = logging.getLogger(__name__)


async def get_current_time(dialog_manager: DialogManager, **kwargs):
    return {"current_time": get_date_time().time()}


async def set_mailing_text(_, __, manager: DialogManager, mailing_text: str):
    manager.dialog_data["mailing_text"] = mailing_text

    await manager.switch_to(MailingSG.select_date)


async def set_mailing_date(_, __, manager: DialogManager, selected_date: date):
    manager.dialog_data["mailing_date"] = str(selected_date)

    await manager.switch_to(MailingSG.select_time)


async def set_mailing_time(message: types.Message, _, manager: DialogManager, mailing_time: str):
    try:
        datetime.strptime(mailing_time, "%H:%M:%S")
    except ValueError:
        await message.answer("Время не в том формате")
        return

    manager.dialog_data["mailing_time"] = mailing_time

    await manager.switch_to(MailingSG.confirm_mailing)


async def confirm_mailing(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    arqredis: ArqRedis = manager.middleware_data.get("arqredis")

    selected_date: str = manager.dialog_data.get("mailing_date")
    mailing_time: str = manager.dialog_data.get("mailing_time")

    date_and_time = datetime.combine(
        datetime.strptime(selected_date, "%Y-%m-%d").date(),
        datetime.strptime(mailing_time, "%H:%M:%S").time(),
    )

    if widget.widget_id == "yes":
        await arqredis.enqueue_job(
            "notify_users",
            _defer_until=date_and_time,
            text=manager.dialog_data.get("mailing_text"),
        )

        logger.info("В планировщик добавлена задача на рассылку")
        await call.answer("Рассылка запланирована")

    elif widget.widget_id == "no":
        await call.answer("Рассылка отменена")

    await manager.done()
