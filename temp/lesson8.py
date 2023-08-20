from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config_data.config import *
from random import randint


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/description')
b3 = KeyboardButton('❤️')
b4 = KeyboardButton('/photo')
b5 = KeyboardButton('/location')
kb.add(b1).row(b2, b3).row(b4, b5)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в наш бот.',
                           parse_mode='HTML',
                           reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['help'])  # readme p.1
async def help_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_CMD,
                           parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['description'])   # readme p.1
async def desc_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Наше приложение добавляет всякую хрень.',
                           parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['photo'])   # readme p.3
async def foto_cmd(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://main-cdn.sbermegamarket.ru/big1/hlr-system/986/168/469/922/185/5/100029280050b0.jpg')
    await message.delete()


@dp.message_handler(commands=['location'])   # readme p.4
async def location_cmd(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=randint(1, 100),
                            longitude=randint(1, 100))
    await message.delete()


@dp.message_handler()   # readme p.2
async def sticker_cmd(message: types.Message):
    if message.text == '❤️':
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker='CAACAgIAAxkBAAEKEAZk36FCJ4UyrjNIxJenCzJMw-4B-wACewADwZxgDNsaH7YdVDaIMAQ')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
