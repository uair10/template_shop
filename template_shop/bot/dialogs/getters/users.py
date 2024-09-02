from aiogram_dialog import DialogManager

from template_shop.core.config import Settings
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.user import UserService


async def get_user_info(
    dialog_manager: DialogManager,
    user_service: UserService,
    order_service: OrderService,
    **kwargs,
):
    config: Settings = dialog_manager.middleware_data.get("config")
    user_id: int = dialog_manager.event.from_user.id

    user = await user_service.get_user_by_telegram_id(user_id)
    user_orders = await order_service.get_user_orders(user_id)

    return {
        "is_admin": user_id in config.tg_bot.admin_ids,
        "user_id": user_id,
        "user_balance": user.balance,
        "orders_count": len(user_orders),
        "reg_date": user.was_registered.date(),
    }
