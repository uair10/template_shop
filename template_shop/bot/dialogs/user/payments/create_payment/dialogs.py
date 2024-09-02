from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Url
from aiogram_dialog.widgets.text import Const, Format

from template_shop.bot.dialogs.getters.currency import usd_rate_getter
from template_shop.bot.dialogs.widgets import LocaleText, StartWithData
from template_shop.bot.states import PaymentSG, PromocodeSG

from .handlers import set_payment_amount, set_payment_method

set_payment_method_window = Window(
    LocaleText("select-payment-method-msg"),
    Button(
        LocaleText("crypto-btn"),
        id="crypto",
        on_click=set_payment_method,
    ),
    Cancel(LocaleText("back-btn")),
    state=PaymentSG.select_method,
)


set_amount_window = Window(
    LocaleText(
        "select-payment-amount-usd-msg",
    ),
    Button(
        Format("{start_data[order_summ]}") + Const("$"),
        id="order_summ",
        on_click=set_payment_amount,
        when=F["start_data"]["order_summ"],
    ),
    TextInput("payment_amount", str, on_success=set_payment_amount),
    Back(LocaleText("back-btn")),
    getter=usd_rate_getter,
    state=PaymentSG.select_amount,
)

check_payment_window = Window(
    LocaleText("payment-msg"),
    LocaleText("payment-msg-in-order", when=F["start_data"]["order_summ"]),
    LocaleText("payment-msg-in-account", when=~F["start_data"]["order_summ"]),
    Cancel(LocaleText("back-to-account-btn"), when=~F["start_data"]["order_summ"]),
    Cancel(LocaleText("back-to-order-btn"), when=F["start_data"]["order_summ"]),
    Url(LocaleText("pay-btn"), Format("{dialog_data[bill_link]}")),
    StartWithData(
        LocaleText("enter-promocode-btn"),
        id="enter_promocode_btn",
        state=PromocodeSG.enter_promocode,
        data_keys=["payment_id"],
    ),
    Back(LocaleText("enter-different-sum-btn"), when=~F["start_data"]["order_summ"]),
    state=PaymentSG.create_payment,
    disable_web_page_preview=True,
)

new_payment_dialog = Dialog(set_payment_method_window, set_amount_window, check_payment_window)
