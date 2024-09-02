from aiogram import types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from template_shop.core.exporters.products_to_xlsx import export_products_to_xlsx
from template_shop.core.utils.date_time import get_date_time
from template_shop.infrastructure.database.services.order import OrderService


async def export_order_products_to_xlsx(call: types.CallbackQuery, _, manager: DialogManager):
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    order_id: int = manager.dialog_data.get("order_id")
    order_service: OrderService = manager.middleware_data.get("order_service")

    order = await order_service.get_order_by_id(order_id, True)
    xlsx_content = export_products_to_xlsx(order.products)

    cur_date = get_date_time(time_format="%Y-%m-%d_%H-%M-%S")
    await call.message.answer_document(
        types.BufferedInputFile(
            xlsx_content,
            filename=f"Products {cur_date}.xlsx",
        ),
        caption=locale.get("excel-info-msg"),
    )
