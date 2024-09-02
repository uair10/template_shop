from sqlalchemy import select

from template_shop.infrastructure.database.models import BotSettings
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class BotSettingsRepoImpl(SQLAlchemyRepo):
    async def get_bot_settings(self) -> BotSettings:
        """Получаем настройки бота"""

        settings: BotSettings | None = await self._session.scalar(select(BotSettings))
        return settings
