import logging
from decimal import Decimal
from typing import Any

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from template_shop.bot.services.tg_helpers import send_tg_message
from template_shop.bot.states import BuyAccountSG
from template_shop.core.config import Settings
from template_shop.infrastructure.database.services.category import CategoryService
from template_shop.infrastructure.database.services.country import CountryService
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.product import ProductService
from template_shop.infrastructure.database.services.statistics import StatsService
from template_shop.infrastructure.database.services.user import UserService

logger = logging.getLogger(__name__)


async def set_template_type(_, widget: Any, manager: DialogManager):
    category_service: CategoryService = manager.middleware_data.get("category_service")
    country_service: CountryService = manager.middleware_data.get("country_service")
    manager.dialog_data["template_type"] = widget.widget_id
    if widget.widget_id == "cards":
        await manager.switch_to(BuyAccountSG.select_products)
        category = await category_service.get_category_by_name("Cards")
        country = await country_service.get_country_by_name("International")
        manager.dialog_data["category_id"] = category.id
        manager.dialog_data["country_id"] = country.id
    else:
        await manager.next()


async def set_category_id(
    _,
    __,
    manager: DialogManager,
    category_id: str,
):
    manager.dialog_data["category_id"] = int(category_id)
    await manager.next()


async def set_country_id(
    _,
    __,
    manager: DialogManager,
    country_id: str,
):
    manager.dialog_data["country_id"] = int(country_id)
    await manager.next()


async def select_product(
    _,
    __,
    manager: DialogManager,
    product_id: str,
):
    manager.dialog_data["product_id"] = int(product_id)
    await manager.next()


async def clear_cart(_, __, manager: DialogManager):
    manager.dialog_data.pop("cart")


async def add_product_to_cart(_, __, manager: DialogManager):
    product_id: int = manager.dialog_data.get("product_id")
    cart: list[int] = manager.dialog_data.get("cart", [])
    cart.append(product_id)
    manager.dialog_data["cart"] = cart
    await manager.back()


async def order_doc_drawing(call: types.CallbackQuery, __, manager: DialogManager):
    bot: Bot = manager.middleware_data.get("bot")
    config: Settings = manager.middleware_data.get("config")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    product_service: ProductService = manager.middleware_data.get("product_service")
    country_service: CountryService = manager.middleware_data.get("country_service")

    product = await product_service.get_product_by_id(manager.dialog_data.get("product_id"))
    country = await country_service.get_country_by_id(product.country_id)

    user_name = call.from_user.username
    if user_name is None:
        user_name = call.from_user.first_name

    await send_tg_message(
        bot,
        config.tg_bot.channel_for_doc_drawing_orders,
        locale.get(
            "new-order-for-drawing",
            product_name=product.name,
            country_name=country.name,
            user_name=user_name,
            user_tg_id=str(call.from_user.id),
        ),
    )
    await call.answer(locale.get("drawing-order-created-msg"), show_alert=True)
    await manager.done()


async def create_order(
    call: types.CallbackQuery,
    _,
    manager: DialogManager,
):
    """Создаем заказ"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    order_service: OrderService = manager.middleware_data.get("order_service")
    product_service: ProductService = manager.middleware_data.get("product_service")
    user_service: UserService = manager.middleware_data.get("user_service")
    stats_service: StatsService = manager.middleware_data.get("stats_service")

    discount_summ = Decimal(manager.dialog_data.get("discount_summ", 0))
    promocode_id: int = manager.dialog_data.get("promocode_id")

    user = await user_service.get_user_by_telegram_id(call.from_user.id)
    cart_products = manager.dialog_data.get("cart")

    products = [await product_service.get_product_by_id(int(product_id)) for product_id in cart_products]
    order_summ = sum((product.price for product in products))
    order_summ -= discount_summ

    if user.balance < order_summ:
        await call.answer(locale.get("not-enough-balance", balance=user.balance))
        return

    order = await order_service.create_order(
        user_tg_id=call.from_user.id,
        order_sum=order_summ,
        products=products,
        promocode_id=promocode_id,
    )
    manager.dialog_data["order_id"] = order.id
    await stats_service.add_stats(orders_created=1)
    await stats_service.add_stats(products_purchased=len(products))

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "new-order-notification",
            order_id=order.id,
            summ=order.summ,
            discount_summ=discount_summ,
        ),
    )

    await call.answer(locale.get("order-created-msg"))

    await manager.next()
