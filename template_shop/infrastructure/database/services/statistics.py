from template_shop.core.utils.date_time import get_date_time
from template_shop.infrastructure.database.models import Statistics
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class StatsService:
    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def add_stats(
        self,
        products_purchased: int = 0,
        orders_created: int = 0,
        users_registered: int = 0,
        payments_paid: int = 0,
    ) -> None:
        """Обновляем/создаем статистику за текущий день"""

        date = get_date_time().replace(hour=0).replace(minute=0).replace(second=0)
        stats: Statistics = await self._uow.stats_repo.acquire_stats_by_date(date)
        if not stats:
            try:
                await self._uow.stats_repo.create_stats(
                    date,
                    products_purchased,
                    orders_created,
                    users_registered,
                    payments_paid,
                )
            except Exception as err:
                await self._uow.rollback()
                raise err
        else:
            stats.products_purchased += products_purchased
            stats.orders_created += orders_created
            stats.users_registered += users_registered
            stats.payments_paid += payments_paid

            await self._uow.stats_repo.update_stats(stats)

        await self._uow.commit()
