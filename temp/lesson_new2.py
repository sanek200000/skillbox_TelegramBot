from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config_data.config import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


class ProfileStatesGroup(StatesGroup):
    photo = State()
    description = State()


def get_kb(buttons: list(), rows=2) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=False,
                             row_width=rows)
    for btn in buttons:
        kb.insert(KeyboardButton(btn))
    return kb


async def start_cmd(message: types.Message):
    global START_KB
    await bot.send_message(chat_id=message.chat.id,
                           text='Welcome!',
                           reply_markup=get_kb(START_KB, 3))


async def kill_cmd(msg: types.Message):
    await msg.answer(text='Работа бота остановлена',
                     reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    raise SystemExit(1)


async def help_cmd(msg: types.Message):
    global HELP_CMD
    await msg.answer(text=HELP_CMD, parse_mode='HTML')
    await msg.delete()


async def cancel_states(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы прервали заполнение анкеты.',
                         reply_markup=get_kb(START_KB))


# FSM
async def create_cmd(msg: types.Message):
    await msg.reply('Создайте свой профайл.\nДля начала загрузите свое фото.',
                    reply_markup=get_kb(['/cancel']))
    await ProfileStatesGroup.photo.set()


async def load_photo(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[0].file_id

    await msg.reply('Расскажи немного о себе.')
    await ProfileStatesGroup.next()


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(chat_id=message.chat.id,
                             photo=data['photo'],
                             caption=f"{data['description']}")

    await message.answer('Ваша анкета успешно создана',
                         reply_markup=get_kb(START_KB, 3))
    await state.finish()


# Register handlers
def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(start_cmd, commands='start')
    dp.register_message_handler(kill_cmd, commands='kill')
    dp.register_message_handler(help_cmd, commands='help')
    dp.register_message_handler(cancel_states, commands='cancel', state='*')

    # FSM
    dp.register_message_handler(create_cmd, commands='create')
    dp.register_message_handler(
        load_photo,
        content_types='photo',
        state=ProfileStatesGroup.photo
    )
    dp.register_message_handler(
        load_description,
        state=ProfileStatesGroup.description
    )


if __name__ == "__main__":
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)
