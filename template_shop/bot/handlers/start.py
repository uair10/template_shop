from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from template_shop.bot.states import ClientSG
from template_shop.core.exceptions.user import UserTgIdNotExist
from template_shop.infrastructure.database.services.user import UserService


async def user_start(message: types.Message, dialog_manager: DialogManager, user_service: UserService):
    """Команда старта для пользователей"""

    user_id = message.from_user.id
    username = message.from_user.username
    if not username:
        username = message.from_user.first_name
    try:
        await user_service.get_user_by_telegram_id(user_id)
    except UserTgIdNotExist:
        await user_service.create_user(
            telegram_id=user_id,
            username=username,
        )

    await dialog_manager.start(ClientSG.start, mode=StartMode.RESET_STACK)
