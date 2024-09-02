from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from template_shop.bot.dialogs.getters.bills import bill_data_getter, user_bills_getter
from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states.user import UserPaymentsSG

from .handlers import display_payment_details

payments_history_window = Window(
    LocaleText("payment-history"),
    ScrollingGroup(
        Select(
            Format("{item.summ}$ {item.created_at}"),
            "user_payments_sel",
            lambda payment: payment.id,
            "user_bills",
            on_click=display_payment_details,
        ),
        width=1,
        height=4,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Cancel(LocaleText("back-btn")),
    state=UserPaymentsSG.payments_history,
    getter=user_bills_getter,
)

payment_details_window = Window(
    LocaleText("payment-details"),
    LocaleText("payment_id", payment_id="{payment_id}"),
    LocaleText("payment_status", status="{status}"),
    LocaleText("payment_summ", payment_summ="{payment_summ}$"),
    LocaleText("created_at", created_at="{created_at}"),
    Back(LocaleText("back-btn")),
    state=UserPaymentsSG.payment_details,
    getter=bill_data_getter,
)

payments_history_dialog = Dialog(payments_history_window, payment_details_window)
