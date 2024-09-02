import logging

from aiogram import Bot
from fluentogram import TranslatorRunner

from template_shop.bot.services.locale import Localizator
from template_shop.bot.services.tg_helpers import send_tg_message
from template_shop.core.models.enums.bill import BillStatus
from template_shop.core.payment_clients.aiocryptopay import AioCryptoPay
from template_shop.core.payment_clients.aiocryptopay.const import InvoiceStatus
from template_shop.core.utils.date_time import get_date_time
from template_shop.infrastructure.database.services.bill import BillService
from template_shop.infrastructure.database.services.bot_settings import BotSettingsService
from template_shop.infrastructure.database.services.user import UserService
from template_shop.worker.exception_handler import exception_handler

logger = logging.getLogger(__name__)


@exception_handler
async def check_bills(
    ctx,
):
    """Проверяем неоплаченные счета"""

    bot: Bot = ctx["bot"]
    fluent: Localizator = ctx["fluent"]
    aiocryptopay: AioCryptoPay = ctx["aiocryptopay"]
    bot_settings_service: BotSettingsService = ctx["bot_settings_service"]
    user_service: UserService = ctx["user_service"]
    bill_service: BillService = ctx["bill_service"]

    bot_settings = await bot_settings_service.get_bot_settings()
    if bot_settings.bills_checker_enabled:
        cur_date = get_date_time()
        bills = await bill_service.get_uncompleted_bills(cur_date, bot_settings.bills_checker_days)
        for bill in bills:
            user = await user_service.get_user_by_telegram_id(bill.user.telegram_id)

            locale: TranslatorRunner = fluent.get_by_locale(user.lang_code)

            invoices = await aiocryptopay.get_invoices(invoice_ids=bill.invoice_id)
            invoice = invoices[0]

            if invoice.status == InvoiceStatus.PAID or invoice.status.lower() == "paid":
                payment_summ = bill.summ
                await bill_service.update_bill_status(bill.id, bill_status=BillStatus.paid)
                if bill.promocode_id:
                    # Добавляем бонус по промокоду
                    promocode_sum = payment_summ / 100 * bill.promocode.amount
                    payment_summ += promocode_sum
                    logger.info(f"Бонус {promocode_sum} $ юзеру {user.telegram_id} по промокоду")
                await user_service.increase_user_balance(user.telegram_id, payment_summ)
                logger.info(f"Пополнил баланс юзеру {user.telegram_id} на сумму {payment_summ} $")
                await send_tg_message(
                    bot,
                    user.telegram_id,
                    locale.get("payment-successful", payment_summ=payment_summ),
                )

            elif invoice.status == InvoiceStatus.EXPIRED or invoice.status.lower() in [
                "rejected",
                "expired",
            ]:
                logger.info(f"Оплата №{bill.id} на сумму {bill.summ} неуспешна")
                await send_tg_message(
                    bot,
                    user.telegram_id,
                    locale.get(
                        "payment-fail",
                        payment_summ=bill.summ,
                        payment_id=bill.id,
                    ),
                )
                await bill_service.update_bill_status(bill.id, bill_status=BillStatus.payment_failed)
