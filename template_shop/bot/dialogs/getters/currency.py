from aiogram_dialog import DialogManager

from template_shop.core.utils.currency import get_rate_usd


async def usd_rate_getter(dialog_manager: DialogManager, **kwargs):
    usd_rate = await get_rate_usd()
    dialog_manager.dialog_data["usd_rate"] = usd_rate

    return {"usd_rate": round(usd_rate, 2)}
