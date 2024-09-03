import logging
from decimal import Decimal

from template_shop.infrastructure.database.models import Product
from template_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def create_product(
        self,
        name: str,
        price: Decimal,
        link: str,
        category_id: int,
        country_id: int,
        preview_image_path: str | None = None,
    ) -> Product:
        """Создаем товар"""
        product = Product(
            name=name,
            price=price,
            link=link,
            category_id=category_id,
            country_id=country_id,
            preview_image_path=preview_image_path,
        )

        try:
            await self._uow.product_repo.create_product(product)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

        logger.info(f"Product №{product.id} was created")

        return product

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self._uow.product_repo.get_product_by_id(product_id)

    async def get_available_products(self, category_id: int, country_id: int) -> list[Product]:
        return await self._uow.product_repo.get_available_products(category_id, country_id)
