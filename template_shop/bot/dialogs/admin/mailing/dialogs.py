from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Calendar, Cancel
from aiogram_dialog.widgets.text import Const, Format

from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states.admin import MailingSG

from .handlers import confirm_mailing, get_current_time, set_mailing_date, set_mailing_text, set_mailing_time

mailing_text_window = Window(
    Const("Введи текст рассылки"),
    TextInput("mailing_text", str, on_success=set_mailing_text),
    Cancel(LocaleText("back-btn")),
    state=MailingSG.mailing_text,
)

select_date_window = Window(
    Const("Выбери дату рассылки"),
    Calendar(id="calendar", on_click=set_mailing_date),
    Back(LocaleText("back-btn")),
    state=MailingSG.select_date,
)

select_time_window = Window(
    Const("Введи время рассылки в формате 23:59:59"),
    Format("Текущее время: <code>{current_time}</code>"),
    TextInput("mailing_time", str, on_success=set_mailing_time),
    Back(LocaleText("back-btn")),
    state=MailingSG.select_time,
    getter=get_current_time,
)

confirm_mailing_window = Window(
    Const("Подтвердить рассылку?"),
    Button(Const("Да"), id="yes", on_click=confirm_mailing),
    Button(Const("Нет"), id="no", on_click=confirm_mailing),
    Back(LocaleText("back-btn")),
    state=MailingSG.confirm_mailing,
)

mailing_dialog = Dialog(
    mailing_text_window,
    select_date_window,
    select_time_window,
    confirm_mailing_window,
)
