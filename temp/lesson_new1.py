from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config_data.config import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup([[KeyboardButton(text='/kill')]],
                         resize_keyboard=True, one_time_keyboard=True)


@dp.message_handler(commands=['kill'])
async def send_stiker(msg: types.Message):
    await msg.answer(text='Работа бота остановлена')
    await msg.delete()
    raise SystemExit(1)


@dp.message_handler(content_types='sticker')   # readme p.1
async def send_stiker(msg: types.Message):
    await msg.answer_sticker(sticker=msg.sticker.file_id)
    await msg.answer(text=msg.sticker.file_id,
                     reply_markup=kb)


@dp.message_handler(content_types='photo')   # readme p.2.4
async def send_stiker(msg: types.Message):
    await msg.answer(text=msg.photo[0].file_id,
                     reply_markup=kb)


@dp.message_handler(lambda msg: not msg.text.count(' '))   # readme p.2.1
async def send_answer(msg: types.Message):
    await msg.answer(text='В вашем сообщении одно слово', reply_markup=kb)


@dp.message_handler(lambda msg: msg.text.count(' '))   # readme p.2.2
async def send_answer(msg: types.Message):
    await msg.answer(text=msg.text*2, reply_markup=kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
