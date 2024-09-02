import datetime
import logging

from template_shop.core.models.enums.bill import BillStatus, PaymentMethod
from template_shop.infrastructure.database.models import Bill
from template_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class BillService:
    """Сервис для работы с платежами пользователя"""

    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_bill_by_id(self, bill_id: int) -> Bill:
        """Получаем платеж по id"""

        return await self._uow.bill_repo.get_bill_by_id(bill_id)

    async def get_user_bills(self, user_tg_id: int) -> list[Bill]:
        """Получаем платежи пользователя"""

        return await self._uow.bill_repo.get_user_bills(user_tg_id)

    async def get_bill_with_promocode(self, user_tg_id: int, promocode_id: int) -> Bill:
        """Получаем платеж юзера с промокодом"""

        return await self._uow.bill_repo.get_bill_with_promocode(user_tg_id, promocode_id)

    async def add_promocode_to_bill(self, bill_id: int, promocode_id: int) -> None:
        """Добавляем промокод к платежу"""

        bill: Bill = await self._uow.bill_repo.get_bill_by_id(bill_id)
        bill.promocode_id = promocode_id

        try:
            await self._uow.bill_repo.update_bill(bill)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

    async def create_bill(
        self,
        payment_method: PaymentMethod,
        summ: float,
        invoice_id: int,
        user_tg_id: int,
    ) -> Bill:
        """
        Создаем платеж пользователя
        @param payment_method: Выбранный метод оплаты
        @param summ: Сумма платежа
        @param invoice_id: Номер платежа в кассе
        @param user_tg_id: Telegram id пользователя
        @return:
        """

        user = await self._uow.user_repo.get_user_by_tg_id(user_tg_id)
        bill = Bill(
            payment_method=payment_method,
            summ=summ,
            invoice_id=invoice_id,
            user_id=user.id,
        )
        try:
            await self._uow.bill_repo.create_bill(bill)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

        logger.info(f"Bill was created: {bill.id}")

        return bill

    async def get_uncompleted_bills(self, cur_date: datetime.datetime, days: int) -> list[Bill]:
        """Получаем неоплаченные счета за выбранный период"""

        return await self._uow.bill_repo.get_uncompleted_bills(cur_date, days)

    async def update_bill_status(self, bill_id: int, bill_status: BillStatus) -> None:
        """Обновляем статус платежа"""

        bill: Bill = await self._uow.bill_repo.get_bill_by_id(bill_id)
        bill.status = bill_status
        await self._uow.bill_repo.update_bill(bill)

        await self._uow.commit()

        logger.info(f"Bill {bill} status was updated. New status: {bill_status}")
