from aiogram import Dispatcher
from aiogram.filters import Command

from template_shop.bot.handlers.errors import setup_error_handlers
from template_shop.bot.handlers.start import user_start
from template_shop.core.config import Settings


def register_handlers(dp: Dispatcher, config: Settings):
    dp.message.register(user_start, Command(commands="start"))
    setup_error_handlers(dp, config.tg_bot.developer_id)
