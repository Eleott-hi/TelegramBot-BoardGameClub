from typing import Any, Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import (
    ManagedRadio,
    SwitchTo,
    Column,
    Multiselect,
    ManagedMultiselect,
)
from database.database import MDB

from windows.states import FilterSG


async def get_values(**kwargs):
    return dict(
        genres=[
            "Any",
            "Strategy",
            "RPG",
            "War",
            "Shooter",
        ]
    )


async def on_click(
    cb: CallbackQuery, widget: ManagedMultiselect, manager: ManagerImpl, value: Any
):
    print(value, flush=True)

    if value == "Any":
        await widget.reset_checked()
    else:
        await widget.set_checked("Any", checked=False)


async def on_state_changed(
    cb: CallbackQuery, widget: ManagedRadio, manager: ManagerImpl, value: str
):
    db: MDB = manager.middleware_data["db"]
    user_mongo: Dict = manager.middleware_data["user_mongo"]

    curr_values = widget.get_checked()
    curr_values = [] if curr_values == ["Any"] else curr_values

    filter_name: str = "genres"
    filters = user_mongo["optional_filters"]

    if len(filters[filter_name]) != len(curr_values):
        filters[filter_name] = curr_values
        await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)


window = Window(
    StaticMedia(
        path="resources/static/filter.jpg",
        type=ContentType.PHOTO,
    ),
    Format("Select genre(s)"),
    Column(
        Multiselect(
            Format("✅ {item}"),
            Format("☑️ {item}"),
            id="genres",
            item_id_getter=lambda x: x,
            items="genres",
            on_click=on_click,
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(Const("⬅️ Back"), id="to_game_menu", state=FilterSG.main),
    state=FilterSG.genre,
    getter=get_values,
)
