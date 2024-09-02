from aiogram_dialog import DialogManager

from template_shop.infrastructure.database.services.product import ProductService


async def cart_getter(dialog_manager: DialogManager, product_service: ProductService, **kwargs):
    cart_products: list[int] = dialog_manager.dialog_data.get("cart", [])

    products = [await product_service.get_product_by_id(product_id) for product_id in cart_products]
    cart_total = sum((product.price for product in products))

    return {
        "cart_total": cart_total,
    }
