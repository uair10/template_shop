from aiogram_dialog import DialogManager

from template_shop.bot.states.user import UserPaymentsSG


async def display_payment_details(_, __, manager: DialogManager, bill_id: str):
    manager.dialog_data["bill_id"] = int(bill_id)

    await manager.switch_to(UserPaymentsSG.payment_details)
