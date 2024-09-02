from typing import Optional

from aiogram_dialog import DialogManager

from template_shop.core.models.enums.promocode import PromocodeType
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.product import ProductService
from template_shop.infrastructure.database.services.promocode import PromocodeService
from template_shop.infrastructure.database.services.user import UserService


async def user_orders_getter(dialog_manager: DialogManager, **kwargs):
    order_service: OrderService = dialog_manager.middleware_data.get("order_service")
    user_orders = await order_service.get_user_orders(dialog_manager.event.from_user.id)

    return {"user_orders": user_orders}


async def order_info_getter(dialog_manager: DialogManager, **kwargs):
    order_service: OrderService = dialog_manager.middleware_data.get("order_service")

    order_id: int = dialog_manager.dialog_data.get("order_id")
    order = await order_service.get_order_by_id(order_id)

    # Нужно для пополнения баланса из заказа
    dialog_manager.dialog_data["order_summ"] = order.summ

    return {
        "order_id": order.id,
        "order_summ": order.summ,
        "was_created": order.created_at.date(),
    }


async def order_summary_getter(
    dialog_manager: DialogManager,
    user_service: UserService,
    product_service: ProductService,
    promocode_service: PromocodeService,
    **kwargs,
):
    """Рассчитываем сумму заказа"""

    user_id: int = dialog_manager.event.from_user.id
    cart_products = dialog_manager.dialog_data.get("cart")

    products = [await product_service.get_product_by_id(int(product_id)) for product_id in cart_products]
    promocode = None
    promocode_id: Optional[int] = dialog_manager.dialog_data.get("promocode_id")
    if promocode_id:
        promocode = await promocode_service.get_promocode_by_id(promocode_id)

    user = await user_service.get_user_by_telegram_id(user_id)

    order_summ = sum((product.price for product in products))

    discount_summ = None
    if promocode and promocode.type == PromocodeType.discount:
        # Уменьшаем сумму заказа при наличии промокода
        discount_summ = (order_summ / 100) * promocode.amount
        order_summ = order_summ - discount_summ
        dialog_manager.dialog_data["discount_summ"] = float(discount_summ)

    dialog_manager.dialog_data["order_summ"] = float(order_summ)
    order_products = "\n".join(f"{product.name} – {product.price}$" for product in products) + "\n"

    return {
        "order_summ": order_summ,
        "discount_summ": discount_summ,
        "order_products": order_products,
        "user_balance": user.balance,
    }
