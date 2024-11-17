from template_shop.infrastructure.database.models import Country
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class CountryService:
    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_countries(self) -> list[Country]:
        return await self._uow.country_repo.get_countries()

    async def get_country_by_id(self, country_id: int) -> Country:
        return await self._uow.country_repo.get_country_by_id(country_id)

    async def get_country_by_name(self, country_name: str) -> Country:
        return await self._uow.country_repo.get_country_by_name(country_name)
