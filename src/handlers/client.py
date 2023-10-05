from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.client_kb import get_kb
from config_data.config import START_KB


async def command_start(msg: types.Message):
    try:
        await msg.answer(text='Приветствую!', reply_markup=get_kb(START_KB, 2))
        await msg.delete()
    except:
        msg.reply('Общение с ботом через ЛС, напишите ему:',
                  'https://t.me/temp_heist2000_bot', sep='\n')


async def command_lowprice(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'lowprice')
    await msg.delete()


async def command_highprice(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'highprice')
    await msg.delete()


async def command_bestdeal(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'bestdeal')
    await msg.delete()


async def command_history(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'history')
    await msg.delete()


async def kill_cmd(msg: types.Message):
    await msg.answer(text='Работа бота остановлена',
                     reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()
    raise SystemExit(1)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    # dp.register_message_handler(command_lowprice, commands=['lowprice'])
    dp.register_message_handler(command_highprice, commands=['highprice'])
    dp.register_message_handler(command_bestdeal, commands=['bestdeal'])
    dp.register_message_handler(command_history, commands=['history'])
    dp.register_message_handler(kill_cmd, commands='kill')
