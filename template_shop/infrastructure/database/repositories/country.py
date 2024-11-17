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
        countries.sort(key=lambda country: country.name)

        return countries

    @exception_mapper
    async def get_country_by_id(self, country_id: int) -> Country:
        query = select(Country).where(Country.id == country_id)
        country: Country | None = await self._session.scalar(query)

        return country

    @exception_mapper
    async def get_country_by_name(self, country_name: str) -> Country:
        query = select(Country).where(Country.name.ilike(country_name))
        country: Country | None = await self._session.scalar(query)

        return country
