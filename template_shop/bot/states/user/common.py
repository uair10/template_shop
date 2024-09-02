from aiogram.fsm.state import State, StatesGroup


class ClientSG(StatesGroup):
    start = State()


class LanguageSG(StatesGroup):
    select_language = State()


class UserProfileSG(StatesGroup):
    show_profile = State()


class UserOrdersSG(StatesGroup):
    orders_history = State()
    order_details = State()


class OrderDetailsSG(StatesGroup):
    order_details = State()


class UserPaymentsSG(StatesGroup):
    payments_history = State()
    payment_details = State()


class PaymentSG(StatesGroup):
    select_method = State()
    select_amount = State()
    create_payment = State()


class PromocodeSG(StatesGroup):
    enter_promocode = State()


class BuyAccountSG(StatesGroup):
    select_country = State()
    select_category = State()
    select_products = State()
    product_info = State()
    overview_order = State()
    order_created = State()
