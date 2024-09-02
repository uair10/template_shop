from sqlalchemy import select

from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Category, Product
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class CategoryRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_category_by_id(self, category_id: int) -> Category:
        query = select(Category).where(Category.id == category_id)
        category: Category | None = await self._session.scalar(query)

        return category

    @exception_mapper
    async def get_categories(self, country_id: int) -> list[Category]:
        """Получаем категории"""

        query = select(Category).join(Category.products).where(Product.country_id == country_id)

        res = await self._session.scalars(query)
        categories: list[Category] = list(res.unique())

        return categories
