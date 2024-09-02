import logging
import re
from typing import Any, Union

from aiogram import Bot, types
from aiogram_dialog import DialogManager

from template_shop.bot.services.locale import Locale
from template_shop.bot.services.tg_helpers import send_tg_message
from template_shop.bot.states import PaymentSG
from template_shop.core.config import Settings
from template_shop.core.models.enums.bill import PaymentMethod
from template_shop.core.payment_clients.aiocryptopay import AioCryptoPay
from template_shop.core.utils.date_time import get_date_time
from template_shop.infrastructure.database.services.bill import BillService

logger = logging.getLogger(__name__)


async def set_payment_method(_, widget: Any, manager: DialogManager):
    manager.dialog_data["payment_method"] = widget.widget_id
    await manager.next()


async def set_payment_amount(
    message: Union[types.CallbackQuery, types.Message],
    widget: Any,
    manager: DialogManager,
    payment_amount: str = None,
):
    aiocryptopay: AioCryptoPay = manager.middleware_data.get("aiocryptopay")
    bill_service: BillService = manager.middleware_data.get("bill_service")
    bot: Bot = manager.middleware_data.get("bot")
    config: Settings = manager.middleware_data.get("config")
    locale: Locale = manager.middleware_data.get("locale")

    order_summ: float = manager.start_data.get("order_summ") if manager.start_data else None

    manager.dialog_data.get("usd_rate")
    payment_method = getattr(PaymentMethod, manager.dialog_data.get("payment_method"))

    # Если в качестве суммы оплаты была выбрана сумма заказа
    if widget.widget_id == "order_summ" and order_summ:
        payment_summ = float(order_summ)
    else:
        if payment_amount.isdigit():
            payment_summ = float(payment_amount)
        else:
            # Обрабатываем подобный ввод 100 $.
            try:
                summ = re.findall("(\d+\S+)", payment_amount)[0]
                summ = summ.replace(",", ".")
                payment_summ = float(summ)
            except (ValueError, IndexError):
                await message.answer(locale.get("summ-wrong-format"))
                return

    try:
        cur_date = get_date_time()

        description = f"{message.from_user.id}_{cur_date}"
        invoice = await aiocryptopay.create_invoice(
            asset="USDT",
            amount=payment_summ,
            description=description,
        )
        invoice_id = invoice.invoice_id

        bill = await bill_service.create_bill(
            payment_method=payment_method,
            summ=payment_summ,
            invoice_id=invoice_id,
            user_tg_id=message.from_user.id,
        )
        logger.info(f"Создан новый счет {invoice_id}. Метод оплаты: {payment_method}")
        logger.info(f"Добавлен новый счет №{bill.id} на сумму {bill.summ} $")

        manager.dialog_data["payment_summ"] = payment_summ
        manager.dialog_data["payment_id"] = bill.id
        manager.dialog_data["bill_link"] = invoice.pay_url

        await manager.switch_to(PaymentSG.create_payment)

    except Exception as e:
        logger.exception(e)
        await message.answer(locale.get("error-msg"))
        await send_tg_message(
            bot,
            config.tg_bot.developer_id,
            f"Ошибка во время создания счета для оплаты: {str(e)}",
        )
