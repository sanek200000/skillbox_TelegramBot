from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/start')
b2 = KeyboardButton('/lowprice')
b3 = KeyboardButton('/highprice')
b4 = KeyboardButton('/bestdeal')
b5 = KeyboardButton('/history')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2, b3).row(b4, b5)