from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from template_shop.infrastructure.database.services.bill import BillService
from template_shop.infrastructure.database.services.bot_settings import BotSettingsService
from template_shop.infrastructure.database.services.category import CategoryService
from template_shop.infrastructure.database.services.country import CountryService
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.product import ProductService
from template_shop.infrastructure.database.services.promocode import PromocodeService
from template_shop.infrastructure.database.services.statistics import StatsService
from template_shop.infrastructure.database.services.user import UserService
from template_shop.infrastructure.database.uow.uow import build_uow


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            uow = build_uow(session)
            data["uow"] = uow
            data["user_service"] = UserService(uow)
            data["bot_settings_service"] = BotSettingsService(uow)
            data["order_service"] = OrderService(uow)
            data["bill_service"] = BillService(uow)
            data["category_service"] = CategoryService(uow)
            data["country_service"] = CountryService(uow)
            data["product_service"] = ProductService(uow)
            data["promocode_service"] = PromocodeService(uow)
            data["stats_service"] = StatsService(uow)

            return await handler(event, data)
