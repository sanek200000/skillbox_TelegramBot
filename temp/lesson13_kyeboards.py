from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/description')
b3 = KeyboardButton(text='Рандомные фото')
b4 = KeyboardButton(text='/kill')
kb.add(b3).add(b1, b2).add(b4)


ikb = InlineKeyboardMarkup()
ib1 = InlineKeyboardButton(text='👍',
                           callback_data='like')
ib2 = InlineKeyboardButton(text='👎',
                           callback_data='dislike')
ib3 = InlineKeyboardButton(text='Следующая рандомная фотография',
                           callback_data='next_photo')
ikb.add(ib1, ib2).add(ib3)
