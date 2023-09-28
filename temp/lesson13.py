from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config_data.config import *
from lesson13_kyeboards import kb, ikb
from random import choice, randint

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


async def onstartup(_):
    print('Бот запущен')


async def random_photo(message: types.Message):
    global PIC_LIST
    await bot.send_photo(chat_id=message.chat.id,
                         photo=choice(PIC_LIST),
                         caption='Нравится ли вам данная фотография?',
                         reply_markup=ikb)


@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Welcome! Ваше местоположение:',
                           reply_markup=kb)
    # await bot.send_location(chat_id=message.chat.id,
    #                        latitude=randint(1, 50),
    #                        longitude=randint(1, 50))
    await message.delete()


@dp.message_handler(commands='kill')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Работа бота остановлена')
    await message.delete()
    raise SystemExit(1)


@dp.message_handler(commands='help')
async def send_cmd(message: types.Message):
    global HELP_CMD
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_CMD,
                           parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands='description')
async def send_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='бот присылает рандомные картинки и заставляет их оцениваать',
                           parse_mode='HTML')
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker='CAACAgIAAxkBAAEKEAZk36FCJ4UyrjNIxJenCzJMw-4B-wACewADwZxgDNsaH7YdVDaIMAQ')
    await message.delete()


@dp.message_handler(Text(equals='Рандомные фото'))
async def send_photo_cmd(message: types.Message):
    await random_photo(message)
    await message.delete()


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer('Вам понравилась данная фотография')
    elif callback.data == 'dislike':
        await callback.answer('Вам не понравилась данная фотография')
    await random_photo(message=callback.message)
    await callback.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=onstartup)
