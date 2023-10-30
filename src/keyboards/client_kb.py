from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_kb(buttons: list, rows=2) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=rows
    )
    for btn in buttons:
        kb.insert(KeyboardButton(btn))
    return kb


def get_ikb(buttons: dict, rows=2) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=rows)

    for key, val in buttons.items():
        ikb.insert(InlineKeyboardButton(text=val, callback_data=key))

    return ikb
