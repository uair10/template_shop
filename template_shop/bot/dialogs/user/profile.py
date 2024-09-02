from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Start

from template_shop.bot.dialogs.getters.users import get_user_info
from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states import PromocodeSG
from template_shop.bot.states.user import PaymentSG, UserOrdersSG, UserPaymentsSG, UserProfileSG

user_profile_window = Window(
    LocaleText("your-account"),
    LocaleText("your-balance", balance="{user_balance}"),
    LocaleText("your-orders-count", orders_count="{orders_count}"),
    LocaleText("registered_date", reg_date="{reg_date}"),
    Start(
        LocaleText("add-balance-btn"),
        id="add_payment_btn",
        state=PaymentSG.select_method,
    ),
    Start(LocaleText("orders-btn"), id="my_orders", state=UserOrdersSG.orders_history),
    Start(
        LocaleText("enter-promocode-btn"),
        id="promocode_btn",
        state=PromocodeSG.enter_promocode,
    ),
    Start(
        LocaleText("payments-btn"),
        id="user_payments",
        state=UserPaymentsSG.payments_history,
    ),
    Cancel(LocaleText("back-btn")),
    state=UserProfileSG.show_profile,
    getter=get_user_info,
)

user_profile_dialog = Dialog(
    user_profile_window,
)
