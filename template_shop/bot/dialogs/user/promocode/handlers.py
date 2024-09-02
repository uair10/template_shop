from typing import Optional

from aiogram import types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from template_shop.bot.services.tg_helpers import answer_msg_with_autodelete
from template_shop.core.models.enums.promocode import PromocodeType
from template_shop.infrastructure.database.services.bill import BillService
from template_shop.infrastructure.database.services.order import OrderService
from template_shop.infrastructure.database.services.promocode import PromocodeService
from template_shop.infrastructure.database.services.user import UserService


async def validate_promocode(message: types.Message, _, manager: DialogManager, promocode_name: str):
    """Проверяем и активируем промокод"""

    locale: TranslatorRunner = manager.middleware_data.get("locale")
    user_service: UserService = manager.middleware_data.get("user_service")
    promocode_service: PromocodeService = manager.middleware_data.get("promocode_service")
    bill_service: BillService = manager.middleware_data.get("bill_service")
    order_service: OrderService = manager.middleware_data.get("order_service")

    payment_id: Optional[int] = manager.dialog_data.get("payment_id")
    order_summ: Optional[float] = manager.dialog_data.get("order_summ")

    promocode = await promocode_service.get_promocode_by_name(promocode_name)

    if not promocode:
        await answer_msg_with_autodelete(message, locale.get("wrong-promocode"))
        return

    if promocode.uses_number >= promocode.limit != 0:
        await answer_msg_with_autodelete(message, locale.get("promocode-usage-limit-reached"))
        return

    user = await user_service.get_user_by_telegram_id(message.from_user.id)

    if promocode.type == PromocodeType.bonus:
        if not payment_id:
            await answer_msg_with_autodelete(message, locale.get("activate-promocode-in-payment"))
            return
        if await bill_service.get_bill_with_promocode(user.telegram_id, promocode.id) and not promocode.reusable:
            await answer_msg_with_autodelete(message, locale.get("promocode-already-used"))
            return

    elif promocode.type == PromocodeType.balance:
        if user in promocode.users and not promocode.reusable:
            await answer_msg_with_autodelete(message, locale.get("promocode-already-used"))
            return

    elif promocode.type == PromocodeType.discount:
        if not order_summ:
            await answer_msg_with_autodelete(message, locale.get("activate-promocode-in-order"))
            return
        if await order_service.get_order_with_promocode(user.telegram_id, promocode.id) and not promocode.reusable:
            # Запрещаем одному и тому же юзеру использовать один промо в разных заказах
            await answer_msg_with_autodelete(message, locale.get("promocode-already-used"))
            return

    if payment_id:
        await bill_service.add_promocode_to_bill(payment_id, promocode.id)

    await user_service.add_promocode_to_user(user.telegram_id, promocode.id)

    await promocode_service.increase_promocode_uses(promocode.id)

    if promocode.type == PromocodeType.balance:
        await user_service.increase_user_balance(message.from_user.id, promocode.amount)
        await message.answer(locale.get("balance-promocode-activated", amount=promocode.amount))
    elif promocode.type == PromocodeType.bonus:
        await message.answer(locale.get("bonus-promocode-activated", amount=promocode.amount))
    elif promocode.type == PromocodeType.discount:
        await message.answer(locale.get("discount-promocode-activated", amount=promocode.amount))

    await manager.done(result={"promocode_id": promocode.id})
