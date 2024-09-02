from sqlalchemy import and_, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from template_shop.core.exceptions.category import CategoryIdNotExist
from template_shop.core.exceptions.common import RepoError
from template_shop.core.exceptions.country import CountryIdNotExist
from template_shop.core.exceptions.product import ProductIdNotExist
from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Product
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class ProductRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_product_by_id(self, product_id: int) -> Product:
        query = select(Product).where(Product.id == product_id).options(joinedload(Product.orders))
        product: Product | None = await self._session.scalar(query)

        if not product:
            raise ProductIdNotExist(product_id)

        return product

    @exception_mapper
    async def get_available_products(self, category_id: int, country_id: int) -> list[Product]:
        """Получаем доступные товары"""

        query = select(Product).where(
            and_(
                Product.category_id == category_id,
                Product.country_id == country_id,
            ),
        )

        res = await self._session.scalars(query)

        products: list[Product] = list(res)

        return products

    @exception_mapper
    async def create_product(self, product: Product) -> None:
        """Создаем товар"""

        self._session.add(product)
        try:
            await self._session.flush((product,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_product(self, product: Product) -> None:
        """Обновляем товар"""

        try:
            await self._session.merge(product)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "fk_product_category_id_category":
                raise CategoryIdNotExist
            case "fk_product_country_id_country":
                raise CountryIdNotExist
            case _:
                raise RepoError from err
