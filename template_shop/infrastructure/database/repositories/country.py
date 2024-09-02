from sqlalchemy import select

from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Country
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class CountryRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_countries(self) -> list[Country]:
        query = select(Country).join(Country.products)

        res = await self._session.scalars(query)
        countries: list[Country] = list(res.unique())

        return countries
