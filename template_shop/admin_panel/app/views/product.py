import os

from flask_admin import form
from slugify import slugify
from werkzeug.utils import secure_filename

from template_shop.admin_panel.app.constants import previews_folder
from template_shop.admin_panel.app.views import MyBaseModelView
from template_shop.infrastructure.database.models import Product


def generate_product_filename(product: Product, file_data, **kwargs):
    """Генерируем название для фото товара"""

    filename, extension = os.path.splitext(file_data.filename)
    filename = filename.replace(filename, slugify(product.name))
    return secure_filename(f"{filename}{extension}")


class ProductModelView(MyBaseModelView):
    column_list = ("id", "name", "price", "link", "country", "category", "order")

    column_filters = (
        "name",
        "price",
        "country",
        "category",
    )

    column_labels = {
        "name": "Название",
        "price": "Цена",
        "link": "Ссылка",
        "country": "Страна",
        "category": "Категория",
        "order": "Заказ",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
    }

    form_extra_fields = {
        "preview_image_path": form.ImageUploadField(
            "Превью документа",
            base_path=previews_folder,
            namegen=generate_product_filename,
            allow_overwrite=True,
            allowed_extensions=("png", "jpg", "jpeg"),
            endpoint="media_bp.previews",
        ),
    }
