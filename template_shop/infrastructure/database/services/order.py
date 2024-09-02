import logging

from template_shop.infrastructure.database.models import Order, Product
from template_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_order_by_id(self, order_id: int, joined: bool = False) -> Order:
        """Получаем заказ по id"""

        return await self._uow.order_repo.get_order_by_id(order_id, joined)

    async def get_user_orders(self, user_tg_id: int) -> list[Order]:
        """Получаем заказы пользователя"""

        return await self._uow.order_repo.get_user_orders(user_tg_id)

    async def get_order_with_promocode(self, user_id: int, promocode_id: int) -> Order:
        """Получаем заказ с промокодом"""

        return await self._uow.order_repo.get_order_with_promocode(user_id, promocode_id)

    async def create_order(
        self,
        order_sum: float,
        user_tg_id: int,
        products: list[Product],
        promocode_id: int | None = None,
    ) -> Order:
        """
        Создаем заказ
        @param order_type: Тип заказа
        @param order_sum: Сумма заказа
        @param user_tg_id: Telegram id пользователя
        @param products: Товары в заказе
        @param promocode_id: Номер промокода
        @return:
        """

        user = await self._uow.user_repo.get_user_by_tg_id(user_tg_id)
        order = Order(
            summ=order_sum,
            user_id=user.id,
            products=products,
            promocode_id=promocode_id,
        )
        user.balance -= order_sum

        try:
            await self._uow.order_repo.create_order(order)
            await self._uow.user_repo.update_user(user)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

        logger.info(f"Order №{order.id} was created")

        return order
