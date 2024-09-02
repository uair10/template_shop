import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, Coroutine, ParamSpec, TypeVar

from template_shop.bot.services.tg_helpers import broadcast
from template_shop.core.config import TgBotConfig
from template_shop.infrastructure.config_loader import load_config

Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
Func = Callable[Param, ReturnType]

logger = logging.getLogger(__name__)


def exception_handler(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            config = load_config(TgBotConfig, "tg_bot")
            logger.exception(f"Error handling job {func}. Error: {str(err)}. Args: {args}. Kwargs: {kwargs}")
            await broadcast(
                args[0].get("bot"),
                [config.developer_id],
                f"Ошибка во время выполнения функции планировщика {func.__name__}: {str(err)}",
            )
            # raise err

    return wrapped
