from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from template_shop.core.exceptions.common import RepoError
from template_shop.core.exceptions.order import OrderIdAlreadyExist
from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Promocode
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class PromocodeRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_promocode_by_id(self, promocode_id: int) -> Promocode:
        query = select(Promocode).where(Promocode.id == promocode_id)
        promocode: Promocode | None = await self._session.scalar(query)

        return promocode

    @exception_mapper
    async def get_promocode_by_name(self, promocode_name: int) -> Promocode:
        query = select(Promocode).where(Promocode.name == promocode_name).options(joinedload(Promocode.users))
        promocode: Promocode | None = await self._session.scalar(query)

        return promocode

    @exception_mapper
    async def update_promocode(self, promocode: Promocode) -> None:
        try:
            await self._session.merge(promocode)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        """Определение ошибки"""

        try:
            match err.__cause__.__cause__.constraint_name:  # type: ignore
                case "pk_order":
                    raise OrderIdAlreadyExist from err
                case _:
                    raise RepoError from err
        except AttributeError:
            raise RepoError from err
