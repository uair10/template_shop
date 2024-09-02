from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from template_shop.infrastructure.database.services.bill import BillService


async def bill_data_getter(dialog_manager: DialogManager, **kwargs):
    bill_id: int = dialog_manager.dialog_data.get("bill_id")
    bill_service: BillService = dialog_manager.middleware_data.get("bill_service")
    locale: TranslatorRunner = dialog_manager.middleware_data.get("locale")

    bill = await bill_service.get_bill_by_id(bill_id)

    return {
        "payment_id": bill.id,
        "payment_summ": bill.summ,
        "status": locale.get(bill.status.value),
        "created_at": bill.created_at,
    }


async def user_bills_getter(dialog_manager: DialogManager, bill_service: BillService, **kwargs):
    user_id: int = dialog_manager.event.from_user.id

    user_bills = await bill_service.get_user_bills(user_id)

    return {
        "user_bills": user_bills,
    }
