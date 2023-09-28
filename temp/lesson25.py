from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import *
from random import randint

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

NUMBER = 0


async def onstartup(_) -> None:
    print('Бот запущен')


def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    ib1 = InlineKeyboardButton(text='Увеличить', callback_data='btn_up')
    ib2 = InlineKeyboardButton(text='Уменьшить', callback_data='btn_down')
    ib3 = InlineKeyboardButton(
        text='Random number', callback_data='btn_random')
    ib4 = InlineKeyboardButton(text='Kill bot', callback_data='btn_kill')
    ikb.add(ib3).add(ib1, ib2).add(ib4)
    return ikb


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f'The current number is {NUMBER}',
                           reply_markup=get_inline_keyboard())
    await message.delete()


@dp.callback_query_handler(lambda x: x.data.startswith('btn'))
async def ikb_cb_handler(callback: types.CallbackQuery):
    global NUMBER
    if callback.data == 'btn_up':
        NUMBER += 1
        await callback.message.edit_text(text=f'The current number is {NUMBER}',
                                         reply_markup=get_inline_keyboard())
    elif callback.data == 'btn_down':
        NUMBER -= 1
        await callback.message.edit_text(text=f'The current number is {NUMBER}',
                                         reply_markup=get_inline_keyboard())
    elif callback.data == 'btn_random':
        NUMBER = randint(1, 100)
        await callback.message.edit_text(text=f'The current number is {NUMBER}',
                                         reply_markup=get_inline_keyboard())
    elif callback.data == 'btn_kill':
        await callback.answer(text='Работа бота остановлена', show_alert=True)
        raise SystemExit(1)
    else:
        1/0

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=onstartup)
