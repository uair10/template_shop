from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start

from template_shop.bot.dialogs.getters.users import get_user_info
from template_shop.bot.dialogs.widgets import LocaleText
from template_shop.bot.states import BuyAccountSG, ClientSG, LanguageSG, UserProfileSG
from template_shop.bot.states.admin import AdminSG

start_window = Window(
    LocaleText("welcome", user="{event.from_user.username}"),
    Start(
        LocaleText("buy-btn"),
        id="buy_btn",
        state=BuyAccountSG.select_template_type,
    ),
    Start(
        LocaleText("change-lang-btn"),
        id="change_lang",
        state=LanguageSG.select_language,
    ),
    Start(LocaleText("profile-btn"), id="user_profile", state=UserProfileSG.show_profile),
    Start(
        LocaleText("admin-btn"),
        id="admin_panel",
        when=F["is_admin"],
        state=AdminSG.admin,
    ),
    state=ClientSG.start,
    getter=get_user_info,
)

start_dialog = Dialog(start_window)
