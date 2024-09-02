from aiogram import Bot

from template_shop.bot.services.tg_helpers import broadcast
from template_shop.core.config import Settings
from template_shop.infrastructure.database.services.user import UserService
from template_shop.worker.exception_handler import exception_handler


@exception_handler
async def notify_users(
    ctx,
    text: str,
) -> None:
    bot: Bot = ctx["bot"]
    config: Settings = ctx["config"]
    user_service: UserService = ctx["user_service"]

    users = await user_service.get_all_users()
    messages_sent, errors_count = await broadcast(bot, users, text)

    await broadcast(
        bot,
        config.tg_bot.admin_ids,
        (
            f"Рассылка закончена\n"
            f"Успешно отправлено сообщений: {messages_sent}\n"
            f"С ошибкой: {errors_count}\n"
            f"Всего пользователей: {len(users)}"
        ),
    )
