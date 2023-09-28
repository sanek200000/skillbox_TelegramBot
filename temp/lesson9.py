from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config_data.config import *

from lesson9_ikb import *   # readme p.6

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/links')
kb.add(b1, b2)


# ikb = InlineKeyboardMarkup(row_width=2)   # readme p.2
# ib1 = InlineKeyboardButton(text='help',
#                           url='https://www.youtube.com/watch?v=5_EHfHbzUCo&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=11')
# ib2 = InlineKeyboardButton(text='url',
#                           url='https://www.youtube.com/watch?v=5_EHfHbzUCo&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=11')
# ikb.add(ib1, ib2)


async def on_startup(_):   # readme p.4
    print('Я был запущен')


@dp.message_handler(commands=['start'])   # readme p.3
async def send_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Wellcome',
                           reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['links'])   # readme p.1
async def send_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='links',
                           reply_markup=ikb)
    await message.delete()


@dp.message_handler(commands=['help'])   # readme p.1
async def send_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_CMD,
                           parse_mode='HTML')
    await message.delete()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
