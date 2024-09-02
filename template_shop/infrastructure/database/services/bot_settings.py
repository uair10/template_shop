from template_shop.infrastructure.database.models import BotSettings
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class BotSettingsService:
    """Сервис для работы с настройками бота"""

    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_bot_settings(self) -> BotSettings:
        """Получаем настройки бота"""

        return await self._uow.bot_settings_repo.get_bot_settings()
