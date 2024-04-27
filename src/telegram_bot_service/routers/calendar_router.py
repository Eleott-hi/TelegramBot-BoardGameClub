import logging
import asyncio
import sys
from datetime import datetime

from libs.calendar.simple_calendar import SimpleCalendar
from libs.calendar.dialog_calendar import DialogCalendar
from libs.calendar.calendar_types import (
    SimpleCalendarCallback,
    DialogCalendarCallback,
)


from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.markdown import hbold

from callbacks.callback_data import Transfer, Screen
from services.utils import create_or_edit_media
from keyboards.builders import inline_builder

router = Router()


@router.callback_query(Transfer.filter(F.to_ == Screen.CALENDAR))
async def nav_cal_handler(query: CallbackQuery, callback_data: Transfer):
    message = query.message

    game_id = callback_data.meta_
    from_ = callback_data.from_
    print(callback_data, flush=True)

    await create_or_edit_media(
        message=message,
        photo="resources/static/booking.jpg",
        caption="Please select a date: ",
        reply_markup=await SimpleCalendar().start_calendar(
            clip_past=True,
            back_data=Transfer(to_=Screen.GAME_MENU, from_=from_, meta_=game_id).pack(),
        ),
        edit=True,
    )

    await query.answer()


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(query: CallbackQuery, callback_data: CallbackData):
    message = query.message

    transfer = callback_data.back_data
    transfer = Transfer.unpack(transfer.replace("|", ":"))
    game_id = transfer.meta_
    from_ = transfer.from_

    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(query, callback_data)

    if selected:
        await create_or_edit_media(
            message=message,
            photo="resources/static/booking.jpg",
            caption="You booked on: " + date.strftime("%d.%m.%Y"),
            reply_markup=inline_builder(
                text=["⬅️ Back", "⬅️ Back to Main Menu"],
                callback_data=[
                    Transfer(to_=Screen.GAME_MENU, from_=from_, meta_=game_id).pack(),
                    Transfer(to_=Screen.MAIN_MENU).pack(),
                ],
                sizes=[1],
            ),
            edit=True,
        )

    await query.answer()