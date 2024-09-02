from aiogram_dialog import DialogManager

from template_shop.infrastructure.database.services.category import CategoryService


async def categories_getter(dialog_manager: DialogManager, category_service: CategoryService, **kwargs):
    categories = await category_service.get_categories(dialog_manager.dialog_data.get("country_id"))

    return {
        "categories": categories,
    }
