from template_shop.infrastructure.database.models import Country
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class CountryService:
    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_countries(self) -> list[Country]:
        return await self._uow.country_repo.get_countries()
