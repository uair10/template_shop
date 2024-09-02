from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    admin = State()


class MailingSG(StatesGroup):
    mailing_text = State()
    select_date = State()
    select_time = State()
    confirm_mailing = State()


class ImportProductsSG(StatesGroup):
    send_products_xlsx = State()
