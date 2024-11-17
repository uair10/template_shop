from template_shop.infrastructure.database.models import Category
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class CategoryService:
    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_category_by_name(self, category_name: str) -> Category:
        return await self._uow.category_repo.get_category_by_name(category_name)

    async def get_category_by_id(self, category_id: int) -> Category:
        return await self._uow.category_repo.get_category_by_id(category_id)

    async def get_categories(self, country_id: int) -> list[Category]:
        return await self._uow.category_repo.get_categories(country_id)
