from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, ErrorEvent, Message, Update
from fluentogram import TranslatorRunner

from template_shop.bot.services.locale import Localizator
from template_shop.core.exceptions.user import UserTgIdNotExist
from template_shop.infrastructure.database.services.user import UserService


class LocaleMiddleware(BaseMiddleware):
    def __init__(self, localizator: Localizator) -> None:
        self._loc: Localizator = localizator

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, Update, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        user_service: UserService = data["user_service"]
        if isinstance(event, Update):
            if event.message:
                user_id = event.message.from_user.id
                user_lang = event.message.from_user.language_code
            else:
                user_id = event.callback_query.from_user.id
                user_lang = event.callback_query.from_user.language_code
        elif isinstance(event, ErrorEvent):
            if event.update.message:
                user_id = event.update.message.from_user.id
                user_lang = event.update.message.from_user.id
            else:
                user_id = event.update.callback_query.from_user.id
                user_lang = event.update.callback_query.from_user.id
        else:
            user_id = event.from_user.id
            user_lang = event.from_user.language_code

        try:
            user = await user_service.get_user_by_telegram_id(user_id)
            user_lang = user.lang_code
        except UserTgIdNotExist:
            pass

        _locale: TranslatorRunner = self._loc.get_by_locale(user_lang)

        data["locale"] = _locale
        data["localizator"] = self._loc

        return await handler(event, data)
