import contextlib
import os

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from template_shop.core.constants import PREVIEWS_FOLDER
from template_shop.infrastructure.database.services.product import ProductService


async def products_getter(dialog_manager: DialogManager, product_service: ProductService, **kwargs):
    category_id: int = dialog_manager.dialog_data.get("category_id")
    country_id: int = dialog_manager.dialog_data.get("country_id")

    products = await product_service.get_available_products(category_id, country_id)

    return {
        "products": products,
    }


async def product_info_getter(dialog_manager: DialogManager, product_service: ProductService, **kwargs):
    product_id: int = dialog_manager.dialog_data.get("product_id")
    product = await product_service.get_product_by_id(product_id)

    product_preview_img = None
    with contextlib.suppress(TypeError):
        if os.path.isfile(file_path := os.path.join(PREVIEWS_FOLDER, product.preview_image_path)):
            product_preview_img = MediaAttachment(
                path=file_path,
                type=ContentType.PHOTO,
            )
        elif "https" in product.preview_image_path:
            product_preview_img = MediaAttachment(
                url=product.preview_image_path,
                type=ContentType.PHOTO,
            )

    return {"product_title": product.name, "product_price": product.price, "product_preview_img": product_preview_img}
