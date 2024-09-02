from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from template_shop.bot.dialogs.getters.orders import user_orders_getter
from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states import UserOrdersSG

from .handlers import display_order_details

orders_history_window = Window(
    LocaleText("orders-history-msg"),
    ScrollingGroup(
        Select(
            Format("№{item.id} {item.summ}$ {item.created_at}"),
            "user_orders_sel",
            lambda order: order.id,
            "user_orders",
            on_click=display_order_details,
        ),
        width=1,
        height=4,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Cancel(
        LocaleText("back-btn"),
    ),
    state=UserOrdersSG.orders_history,
    getter=user_orders_getter,
)

orders_history_dialog = Dialog(
    orders_history_window,
)
