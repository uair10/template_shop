from sqlalchemy import and_, desc, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from template_shop.core.exceptions.common import RepoError
from template_shop.core.exceptions.order import OrderIdAlreadyExist
from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import Order, User
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class OrderRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_order_by_id(self, order_id: int, joined: bool = False) -> Order:
        """Получаем заказ по id"""

        query = select(Order).where(Order.id == order_id)
        if joined:
            query = query.options(joinedload(Order.products))

        order: Order | None = await self._session.scalar(query)

        return order

    @exception_mapper
    async def get_user_orders(self, user_tg_id: int) -> list[Order]:
        """Получаем заказы пользователя"""

        query = (
            select(Order).outerjoin(Order.user).where(User.telegram_id == user_tg_id).order_by(desc(Order.created_at))
        )

        res = await self._session.scalars(query)

        orders: list[Order] = list(res)

        return orders

    @exception_mapper
    async def get_order_with_promocode(self, user_tg_id: int, promocode_id: int) -> Order:
        query = (
            select(Order)
            .outerjoin(Order.user)
            .where(and_(User.telegram_id == user_tg_id, Order.promocode_id == promocode_id))
        )

        order: Order | None = await self._session.scalar(query)

        return order

    @exception_mapper
    async def create_order(self, order: Order) -> None:
        """Создаем заказ"""

        self._session.add(order)
        try:
            await self._session.flush((order,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_order(self, order: Order) -> None:
        """Обновляем заказ"""

        try:
            await self._session.merge(order)
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
