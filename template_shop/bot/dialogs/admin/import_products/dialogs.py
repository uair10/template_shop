from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const

from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states.admin import ImportProductsSG

from .handlers import process_products_file

send_products_xlsx_window = Window(
    Const("Отправьте excel файл с товарами как в образце.\n\n" "В образце заполнены только необходимые поля"),
    StaticMedia(path="resources/import_example.xlsx", type=ContentType.DOCUMENT),
    MessageInput(process_products_file, ContentType.DOCUMENT),
    Cancel(LocaleText("back-btn")),
    state=ImportProductsSG.send_products_xlsx,
)

import_products_dialog = Dialog(send_products_xlsx_window)
