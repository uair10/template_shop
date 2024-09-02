from aiogram import Dispatcher

from template_shop.bot.dialogs import admin, user


def register_dialogs(dp: Dispatcher):
    user.register_user_dialogs(dp)
    admin.register_admin_dialogs(dp)
