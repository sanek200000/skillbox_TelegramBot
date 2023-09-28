from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from config_data.config import *

from lessonORM import create_profile

STORAGE = MemoryStorage()
START_KB = ['/create', '/help', '/kill']

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=STORAGE)


class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


def get_kb(buttons: list()) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=True,
                             row_width=2)
    for btn in buttons:
        kb.insert(KeyboardButton(btn))
    return kb


# START
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Welcome!',
                           reply_markup=get_kb(START_KB))


# KILL
@dp.message_handler(commands='kill')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Работа бота остановлена')
    await message.delete()
    raise SystemExit(1)


# HELP
@dp.message_handler(commands='help')
async def send_cmd(message: types.Message):
    global HELP_CMD
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_CMD,
                           parse_mode='HTML')
    await message.delete()


# CANCEL
@dp.message_handler(commands='cancel', state='*')
async def cancel_states(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы прервали заполнение анкеты.',
                         reply_markup=get_kb(START_KB))


# CREATE
@dp.message_handler(commands='create')
async def send_cmd(message: types.Message):
    await message.reply('Создайте свой профайл.\nДля начала загрузите свое фото.',
                        reply_markup=get_kb(['/cancel']))
    await ProfileStatesGroup.photo.set()


# STATES.not photo
@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo)
async def check_photo(message: types.Message):
    await message.reply('Это не фотография!')


# STATES.photo
@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply('Теперь отправь свое имя.')
    await message.delete()
    await ProfileStatesGroup.next()


# STATES.name
@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Сколько тебе лет?')
    await ProfileStatesGroup.next()


# STATES.age
@dp.message_handler(state=ProfileStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('Расскажи немного о себе.')
    await ProfileStatesGroup.next()


# STATES.description
@dp.message_handler(state=ProfileStatesGroup.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(chat_id=message.chat.id,
                             photo=data['photo'],
                             caption=f"{data['name']}, {data['age']}\n{data['description']}")

    create_profile(user_id=message.from_user.id,
                   name=data['name'],
                   photo=data['photo'],
                   age=int(data['age']),
                   description=data['description'])

    await message.answer('Ваша анкета успешно создана',
                         reply_markup=get_kb(START_KB))
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
