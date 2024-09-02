import asyncio
import contextlib
import logging
from typing import List, Tuple

from aiogram import Bot, exceptions, types
from aiogram.types import BufferedInputFile, FSInputFile

from template_shop.infrastructure.database.models import User

logger = logging.getLogger(__name__)


async def send_tg_message(
    bot: Bot,
    user_id: int,
    text: str,
    disable_notification: bool = False,
    **kwargs,
) -> bool | types.Message:
    """Безопасно отправляем сообщение пользователю"""

    try:
        msg = await bot.send_message(user_id, text, disable_notification=disable_notification, **kwargs)
    except exceptions.TelegramForbiddenError:
        logger.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_tg_message(bot, user_id, text)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return msg
    return False


async def send_document(
    bot: Bot,
    user_id,
    file: BufferedInputFile | FSInputFile | str,
    caption: str,
    disable_notification: bool = False,
) -> bool:
    """Безопасно отправляем документ пользователю"""

    try:
        await bot.send_document(
            user_id,
            file,
            caption=caption,
            disable_notification=disable_notification,
        )
    except exceptions.TelegramForbiddenError:
        logger.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_document(bot, user_id, file, caption)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(
    bot: Bot,
    users: List[int | User],
    text: str,
    file: BufferedInputFile | FSInputFile | str = None,
) -> Tuple[int, int]:
    """
    Рассылка по пользователям
    :param bot: aiogram.Bot instance
    :param text: Текст для отправки
    :param file: Input file или file_id для отправки
    :param users: Список telegram id или список Users
    :return: Успешно отправлено сообщений, сообщений с ошибкой
    """
    messages_sent = 0
    errors_count = 0

    try:
        for user in users:
            if isinstance(user, User):
                user = user.telegram_id
            if file:
                if await send_document(bot, user, file, caption=text):
                    messages_sent += 1
                else:
                    errors_count += 1
            else:
                if await send_tg_message(bot, user, text):
                    messages_sent += 1
                else:
                    errors_count += 1
            await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info(
            f"{messages_sent} messages successful sent. With errors: {errors_count}. Planned to send total: {len(users)}",
        )

    return messages_sent, errors_count


async def delete_msg(msg: types.Message) -> None:
    """Безопасно удаляем сообщение"""

    with contextlib.suppress(exceptions.TelegramBadRequest):
        await msg.delete()


async def answer_msg_with_autodelete(message: types.Message, text: str, seconds: int = 2) -> None:
    """
    Отвечаем на сообщение с автоудалением
    @param message: Сообщение, на которое нужно ответить
    @param text: Текст ответа
    @param seconds: Через сколько секунд удалить ответ
    @return:
    """

    msg = await message.answer(text)
    await asyncio.sleep(seconds)
    await delete_msg(msg)


async def send_msg_with_autodelete(bot: Bot, user_id: int, text: str, seconds: int = 2) -> None:
    """
    Отправляем сообщение с автоудалением
    @param bot: Инстанс бота
    @param user_id: Telegram id пользователя
    @param text: Текст сообщения
    @param seconds: Через сколько секунд удалить ответ
    @return:
    """

    msg = await send_tg_message(bot, user_id=user_id, text=text)
    await asyncio.sleep(seconds)
    await delete_msg(msg)
