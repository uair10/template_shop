from aiogram import Dispatcher

from .import_products import import_products_dialog
from .mailing import mailing_dialog
from .start import features_dialog


def register_admin_dialogs(dp: Dispatcher):
    dp.include_router(features_dialog)
    dp.include_router(mailing_dialog)
    dp.include_router(import_products_dialog)
