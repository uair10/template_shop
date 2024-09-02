import datetime

from sqlalchemy import and_, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from template_shop.core.exceptions.common import RepoError
from template_shop.core.exceptions.order import OrderIdAlreadyExist
from template_shop.core.models.enums.bill import BillStatus
from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Bill, User
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class BillRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_bill_by_id(self, bill_id: int) -> Bill:
        """Получаем платеж по id"""

        query = select(Bill).where(Bill.id == bill_id).with_for_update()
        bill: Bill | None = await self._session.scalar(query)

        return bill

    @exception_mapper
    async def get_user_bills(self, user_tg_id: int) -> list[Bill]:
        """Получаем платежи пользователя"""

        query = select(Bill).outerjoin(Bill.user).where(User.telegram_id == user_tg_id)

        res = await self._session.scalars(query)
        bills: list[Bill] = list(res)

        return bills

    @exception_mapper
    async def get_bill_with_promocode(self, user_tg_id: int, promocode_id: int) -> Bill:
        """Получаем платеж юзера с промокодом"""

        query = (
            select(Bill)
            .outerjoin(Bill.user)
            .where(and_(User.telegram_id == user_tg_id, Bill.promocode_id == promocode_id))
        )
        bill: Bill | None = await self._session.scalar(query)

        return bill

    @exception_mapper
    async def get_uncompleted_bills(self, cur_date: datetime.datetime, days: int) -> list[Bill]:
        """Получаем неоплаченные счета за выбранный период"""

        query = (
            select(Bill).where(
                and_(
                    Bill.status == BillStatus.waiting_payment,
                    Bill.created_at.between(
                        cur_date - datetime.timedelta(days=days),
                        cur_date + datetime.timedelta(days=days),
                    ),
                ),
            )
        ).options(joinedload(Bill.user), joinedload(Bill.promocode))

        res = await self._session.scalars(query)
        bills: list[Bill] = list(res)

        return bills

    @exception_mapper
    async def create_bill(self, bill: Bill) -> None:
        """Создаем платеж"""

        self._session.add(bill)
        try:
            await self._session.flush((bill,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_bill(self, bill: Bill) -> None:
        """Обновляем платеж"""

        try:
            await self._session.merge(bill)
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
