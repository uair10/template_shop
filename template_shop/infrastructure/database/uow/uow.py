from sqlalchemy.ext.asyncio import AsyncSession

from template_shop.infrastructure.database import repositories as repo
from template_shop.infrastructure.database.uow.base import SQLAlchemyBaseUoW


class SQLAlchemyUoW(SQLAlchemyBaseUoW):
    def __init__(
        self,
        *,
        session: AsyncSession,
        user_repo: repo.UserRepoImpl,
        bot_settings_repo: repo.BotSettingsRepoImpl,
        order_repo: repo.OrderRepoImpl,
        bill_repo: repo.BillRepoImpl,
        category_repo: repo.CategoryRepoImpl,
        country_repo: repo.CountryRepoImpl,
        product_repo: repo.ProductRepoImpl,
        promocode_repo: repo.PromocodeRepoImpl,
        stats_repo: repo.StatsRepoImpl,
    ) -> None:
        self.user_repo = user_repo
        self.bot_settings_repo = bot_settings_repo
        self.order_repo = order_repo
        self.bill_repo = bill_repo
        self.category_repo = category_repo
        self.country_repo = country_repo
        self.product_repo = product_repo
        self.promocode_repo = promocode_repo
        self.stats_repo = stats_repo

        super().__init__(session=session)


def build_uow(session: AsyncSession):
    return SQLAlchemyUoW(
        session=session,
        user_repo=repo.UserRepoImpl(session),
        bot_settings_repo=repo.BotSettingsRepoImpl(session),
        order_repo=repo.OrderRepoImpl(session),
        bill_repo=repo.BillRepoImpl(session),
        category_repo=repo.CategoryRepoImpl(session),
        country_repo=repo.CountryRepoImpl(session),
        product_repo=repo.ProductRepoImpl(session),
        promocode_repo=repo.PromocodeRepoImpl(session),
        stats_repo=repo.StatsRepoImpl(session),
    )
