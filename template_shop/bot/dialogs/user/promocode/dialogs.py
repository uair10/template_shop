from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel

from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states import PromocodeSG

from ...extras import copy_start_data_to_ctx
from .handlers import validate_promocode

enter_promocode_window = Window(
    LocaleText("enter-promocode"),
    TextInput("promocode_value", str, on_success=validate_promocode),
    Cancel(LocaleText("back-btn")),
    state=PromocodeSG.enter_promocode,
)

promocode_dialog = Dialog(
    enter_promocode_window,
    on_start=copy_start_data_to_ctx,
)
