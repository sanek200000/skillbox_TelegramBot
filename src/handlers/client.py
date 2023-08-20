from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую!', reply_markup=kb_client)
        await message.delete()
    except:
        message.reply('Общение с ботом через ЛС, напишите ему:', 'https://t.me/temp_heist2000_bot', sep='\n')
        
async def command_lowprice(message: types.Message):
    await bot.send_message(message.from_user.id, 'lowprice')
    await message.delete()
        
async def command_highprice(message: types.Message):
    await bot.send_message(message.from_user.id, 'highprice')
    await message.delete()
    
async def command_bestdeal(message: types.Message):
    await bot.send_message(message.from_user.id, 'bestdeal')
    await message.delete()
    
async def command_history(message: types.Message):
    await bot.send_message(message.from_user.id, 'history')
    await message.delete()
    
    
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_lowprice, commands=['lowprice'])
    dp.register_message_handler(command_highprice, commands=['highprice'])
    dp.register_message_handler(command_bestdeal, commands=['bestdeal'])
    dp.register_message_handler(command_history, commands=['history'])
    
    
    
    
    