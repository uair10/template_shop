from typing import List, Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import Data, DialogManager, StartMode
from aiogram_dialog.widgets.common.when import WhenCondition
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.kbd.button import Button, OnClick
from aiogram_dialog.widgets.text import Text

from template_shop.bot.services.locale import Locale


class LocaleText(Text):
    def __init__(
        self,
        i18n_var_name: str,
        when: WhenCondition = None,
        localizator_name="locale",
        **kwargs,
    ) -> None:
        super().__init__(when=when)
        self.v_name = i18n_var_name
        self._kwargs = kwargs
        self._l_name = localizator_name

    async def _render_text(
        self,
        data: dict,
        manager: DialogManager,
    ) -> str:
        mw_d = manager._data
        locale: Locale = mw_d.get(self._l_name)
        data_to_pass = {}

        data_to_pass.update(data)

        for k, v in self._kwargs.items():
            if not isinstance(v, str):
                data_to_pass[k] = v
                continue
            try:
                data_to_pass[k] = v.format_map(data)
            except KeyError:
                data_to_pass[k] = "%nodata%"

        res = locale.get(self.v_name, **data_to_pass)
        if res is None:
            return f"[{self.v_name}]: locale error, check localization files"
        return res


class StartWithData(Start):
    """Виджет для передачи ключей dialog_data в новый диалог"""

    def __init__(
        self,
        text: Text,
        id: str,
        state: State,
        data_keys: List[str],
        data: Data = None,
        on_click: Optional[OnClick] = None,
        mode: StartMode = StartMode.NORMAL,
        when: WhenCondition = None,
    ) -> None:
        super().__init__(text=text, on_click=self._on_click, id=id, when=when, state=state)
        self.text = text
        self.start_data = data or {}
        self.user_on_click = on_click
        self.state = state
        self.mode = mode
        self.data_keys = data_keys

    async def _on_click(self, callback: CallbackQuery, button: Button, manager: DialogManager):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)

        start_data = {}
        for key in self.data_keys:
            value = manager.dialog_data.get(key)
            if not value and manager.start_data:
                value = manager.start_data.get(key)
            if not value:
                raise ValueError(f"Key {key} not found in dialog_data or start_data")

            start_data[key] = value
        await manager.start(self.state, start_data, self.mode)
