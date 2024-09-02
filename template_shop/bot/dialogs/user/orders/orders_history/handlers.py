from aiogram_dialog import DialogManager

from template_shop.bot.states import OrderDetailsSG


async def display_order_details(_, __, manager: DialogManager, order_id: str):
    await manager.start(OrderDetailsSG.order_details, {"order_id": int(order_id)})
