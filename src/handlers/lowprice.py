from aiogram import types, Dispatcher, executor
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_kb import get_kb, get_ikb
from config_data.config import START_KB, NUM_HOTELS_KB, YESNO_KB, NUM_PHOTOS_KB
from requests_api.get_cities import parse_cities
from loguru import logger


@logger.catch
class ProfileStatesGroup(StatesGroup):
    city = State()
    get_location = State()
    num_hotels = State()
    is_photo = State()
    num_photos = State()


@logger.catch
async def cancel_states(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы прервали поиск отелей.',
                         reply_markup=get_kb(START_KB))


@logger.catch
async def lowprice_cmd(msg: types.Message):
    await msg.reply('Введите название города.',
                    reply_markup=get_kb(['/cancel']))
    await ProfileStatesGroup.city.set()


@logger.catch
async def get_city(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = msg.text.lower()
        logger.info(f'{data = }')

        cities = parse_cities(city=data['city'])
        if cities:
            await msg.answer(text='Выберите количество отелей в выборке.',
                             reply_markup=get_ikb(NUM_HOTELS_KB, 5))
            await ProfileStatesGroup.next()

    # await msg.answer(text='Выберите количество отелей в выборке.',
    #                 reply_markup=get_ikb(NUM_HOTELS_KB, 5))
    # await ProfileStatesGroup.next()


@logger.catch
async def get_location(msg: types.Message, state: FSMContext):
    pass


@logger.catch
async def ask_is_photo(clb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['num_hotels'] = clb.data
        print(data)

    await clb.message.edit_text(text='Показать фото отеля?',
                                reply_markup=get_ikb(YESNO_KB))
    await ProfileStatesGroup.next()


@logger.catch
async def add_num_photos(clb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['is_photo'] = clb.data
        print(data)

    await clb.message.edit_text(text='Выберите количество фото для отеля.',
                                reply_markup=get_ikb(NUM_PHOTOS_KB, 5))
    await ProfileStatesGroup.next()


@logger.catch
async def finish_fsm(clb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['num_photos'] = clb.data
        print(data.as_dict)

    await clb.message.edit_text(text=f'Список отелей: {data._data}')
    await state.finish()


@logger.catch
def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_states, commands='cancel', state='*')
    dp.register_message_handler(lowprice_cmd, commands='lowprice')
    dp.register_message_handler(get_city, state=ProfileStatesGroup.city)
    dp.register_callback_query_handler(get_location,
                                       state=ProfileStatesGroup.get_location)
    dp.register_callback_query_handler(ask_is_photo,
                                       state=ProfileStatesGroup.num_hotels)
    dp.register_callback_query_handler(add_num_photos, lambda clb: int(clb.data),
                                       state=ProfileStatesGroup.is_photo)
    dp.register_callback_query_handler(finish_fsm, lambda clb: not int(clb.data),
                                       state=ProfileStatesGroup.is_photo)
    dp.register_callback_query_handler(finish_fsm,
                                       state=ProfileStatesGroup.num_photos)


if __name__ == "__main__":
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)
