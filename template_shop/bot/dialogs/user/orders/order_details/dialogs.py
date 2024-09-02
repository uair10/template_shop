from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel

from template_shop.bot.dialogs.extras import copy_start_data_to_ctx
from template_shop.bot.dialogs.getters.orders import order_info_getter
from template_shop.bot.dialogs.user.orders.order_details.handlers import export_order_products_to_xlsx
from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states import OrderDetailsSG

order_details_window = Window(
    LocaleText("order-overview"),
    LocaleText("order-summ", order_summ="{order_summ}"),
    LocaleText("order-was-created", was_created="{was_created}"),
    Button(
        LocaleText("export-to-xlsx"),
        id="export_products",
        on_click=export_order_products_to_xlsx,
    ),
    Cancel(LocaleText("back-btn")),
    state=OrderDetailsSG.order_details,
    getter=order_info_getter,
)

order_details_dialog = Dialog(order_details_window, on_start=copy_start_data_to_ctx)
