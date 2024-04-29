from copy import deepcopy
import datetime
from math import ceil
from typing import Any, Dict

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Start,
    Group,
    Row,
    Cancel,
    Next,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


from windows.states import ProfileSG
from aiogram_dialog.widgets.kbd import (
    Button,
    ScrollingGroup,
    Select,
    Column,
    CalendarConfig,
)
from aiogram_dialog.widgets.text import Const, Format
from database.database import MDB
from aiogram_dialog.manager.manager import ManagerImpl


async def get_data(dialog_manager: ManagerImpl, **kwargs):
    print(dialog_manager.event.from_user.full_name, flush=True)

    user_name: str = dialog_manager.event.from_user.full_name
    return dict(user_name=user_name)


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/profile.jpg",
            type=ContentType.PHOTO,
        ),
        Format("Hello, {user_name}!"),
        SwitchTo(Const("Bookings"), id="bookings", state=ProfileSG.bookings),
        SwitchTo(Const("Collections"), id="collections", state=ProfileSG.collections),
        Cancel(Const("⬅️ Back to menu"), id="cancel"),
        state=ProfileSG.main,
        getter=get_data,
    ),
    Window(
        StaticMedia(
            path="resources/static/profile.jpg",
            type=ContentType.PHOTO,
        ),
        Const("Here is your collections"),
        SwitchTo(Const("⬅️ Back"), id="cancel", state=ProfileSG.main),
        state=ProfileSG.collections,
        # getter=get_data,
    ),
    Window(
        StaticMedia(
            path="resources/static/profile.jpg",
            type=ContentType.PHOTO,
        ),
        Const("Here is your bookings"),
        SwitchTo(Const("⬅️ Back"), id="cancel", state=ProfileSG.main),
        state=ProfileSG.bookings,
        # getter=get_data,
    ),
)
