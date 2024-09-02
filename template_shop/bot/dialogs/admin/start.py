from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from template_shop.bot.states.admin import AdminSG, ImportProductsSG, MailingSG
from template_shop.bot.states.user import ClientSG

features_window = Window(
    Const("Привет, админ! Выбери нужную опцию:"),
    Start(
        Const("Отправить рассылку"),
        id="mailing",
        state=MailingSG.mailing_text,
    ),
    Start(
        Const("Импортировать товары"),
        id="import_products",
        state=ImportProductsSG.send_products_xlsx,
    ),
    Start(
        Const("⬅️ Назад"),
        id="back_to_menu",
        state=ClientSG.start,
    ),
    state=AdminSG.admin,
)

features_dialog = Dialog(features_window)
