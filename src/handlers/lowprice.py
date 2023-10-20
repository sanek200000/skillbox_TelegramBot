from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import get_kb, get_ikb
from requests_api.get_cities import parse_cities
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_data.config import START_KB, NUM_HOTELS_KB, YESNO_KB, NUM_PHOTOS_KB
from loguru import logger
from requests_api.get_hotels import parse_hotels
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta

from handlers.print_result import get_hotels

# TODO delete HOTELS and get_hotels()
HOTELS = [
    {
        "hotel_id": "478852",
        "hotel_name": "Viktorija Hotel",
        "price": 29,
        "checkInDate": "10-10-2023",
        "checkOutDate": "12-10-2023",
        "timedelta": 2,
        "address": "ул. A. Caka, 55, Рига, LV-1011",
        "destinationInfo": 1.77,
        "photos": [
            "https://images.trvl-media.com/lodging/1000000/480000/478900/478852/97f4d32c.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/1000000/480000/478900/478852/8c57d145.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/1000000/480000/478900/478852/3b860c8b.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/1000000/480000/478900/478852/c3a1a2bc.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/1000000/480000/478900/478852/7a6a1789.jpg?impolicy=resizecrop&rw=500&ra=fit",
        ],
    },
    {
        "hotel_id": "1943009",
        "hotel_name": "Dodo Hotel",
        "price": 35,
        "checkInDate": "10-10-2023",
        "checkOutDate": "12-10-2023",
        "timedelta": 2,
        "address": "ул. Jersikas, 1, Рига, 1003",
        "destinationInfo": 2.47,
        "photos": [
            "https://images.trvl-media.com/lodging/2000000/1950000/1943100/1943009/4f906a5e.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/2000000/1950000/1943100/1943009/bd22f8b0.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/2000000/1950000/1943100/1943009/57e23e9c.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/2000000/1950000/1943100/1943009/ba6b5c8b.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/2000000/1950000/1943100/1943009/35e648e6.jpg?impolicy=resizecrop&rw=500&ra=fit",
        ],
    },
    {
        "hotel_id": "10039243",
        "hotel_name": "Mosaic Hotel",
        "price": 36,
        "checkInDate": "10-10-2023",
        "checkOutDate": "12-10-2023",
        "timedelta": 2,
        "address": "ул. Elizabetes, 31а, стр. 601, во дворе дома 31а, Рига, LV-1010",
        "destinationInfo": 0.98,
        "photos": [
            "https://images.trvl-media.com/lodging/11000000/10040000/10039300/10039243/a4d9613b.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/11000000/10040000/10039300/10039243/9eb946d4.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/11000000/10040000/10039300/10039243/b2767870.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/11000000/10040000/10039300/10039243/6b52cce0.jpg?impolicy=resizecrop&rw=500&ra=fit",
            "https://images.trvl-media.com/lodging/11000000/10040000/10039300/10039243/91e07444.jpg?impolicy=resizecrop&rw=500&ra=fit",
        ],
    },
]


# @logger.catch
# async def get_hotels(msg: Message) -> Message | None:
#    for hotel in HOTELS:
#        price = hotel.get("price")
#        days = hotel.get("timedelta")

#        try:
#            fullprice = "{:.2f}".format(float(price) * int(days))
#        except Exception as ex:
#            logger.error(f"{ex} \n{price = } \n{days = }")
#            fullprice = None

#        about_hotel = "\n".join(
#            [
#                f'Отель: {hotel.get("hotel_name")}',
#                f'Адрес: {hotel.get("address")}',
#                f'Удаленность от центра: {hotel.get("destinationInfo")} км.',
#                f'Дата заезда: {hotel.get("checkInDate")}',
#                f'Дата выезда: {hotel.get("checkOutDate")}',
#                f"Цена за ночь: ${price}",
#                f"Полная стоимость: ${fullprice}",
#            ]
#        )
#        await msg.answer(text=about_hotel)

#        images = hotel.get("photos")
#        if images:
#            photos_media_list = [InputMediaPhoto(media=photo) for photo in images]
#            logger.info(f"{photos_media_list = }")

#            await bot.send_media_group(chat_id=msg.chat.id, media=photos_media_list)
#        else:
#            await msg.answer(text="NO PHOTOS")


class ProfileStatesGroup(StatesGroup):
    """Машина состояний"""

    get_city = State()
    amount_hotels = State()
    get_checkInDate = State()
    get_checkOutDate = State()
    is_photo = State()
    amount_photos = State()
    fin = State()


@logger.catch
async def cancel_states(msg: Message, state: FSMContext) -> Message | None:
    """
    Прерывает выполнение машины состояний ProfileStatesGroup на любом шаге
    """

    if state is None:
        return
    await state.finish()
    await msg.answer("Вы прервали поиск отелей.", reply_markup=get_kb(START_KB))


@logger.catch
async def get_city(msg: Message) -> Message | None:
    """
    Функция просит ввести город.
    Входит в машину состояний ProfileStatesGroup,
    возвращает название города: Message
    """

    await msg.reply("Введите название города.", reply_markup=get_kb(["/cancel"]))
    await ProfileStatesGroup.get_city.set()


@logger.catch
async def get_location(msg: Message, state: FSMContext) -> CallbackQuery | None:
    """
    Функция получает город из get_city,
    ищет совпадения на rapidapi.com,
    просит уточнить, в какой именно локации находится город.
    Переходит на следующий уровень МС, передает локацию: CallbackQuery
    """

    # async with state.proxy() as data:
    city = msg.text.lower()
    logger.info(f"{city = }")

    cities = parse_cities(city=city)
    if cities:
        cities["Отмена"] = "cancel"  # TODO дописать cancel
        await msg.answer(text="Выберите локацию.", reply_markup=get_ikb(cities, 1))
        await ProfileStatesGroup.next()
    else:
        await msg.answer(
            text="Неправильно введен город, попробуйте еще раз.",
            reply_markup=get_kb(["/cancel"]),
        )


@logger.catch
async def amount_hotels(clb: CallbackQuery, state: FSMContext) -> CallbackQuery | None:
    """
    Функция получает локацию: CallbackQuery из get_location(),
    просит ввести количество отелей в конечной выборке.
    Переходит на следующий уровень МС, передает количество отелей: CallbackQuery
    """
    async with state.proxy() as data:
        data["city_id"] = clb.data
        logger.info(f'{data["city_id"] = }')

    await clb.message.edit_text(
        text="Выберите количество отелей в выборке.",
        reply_markup=get_ikb(NUM_HOTELS_KB, 5),
    )
    await ProfileStatesGroup.next()


@logger.catch
async def get_checkInDate(
    clb: CallbackQuery, state: FSMContext
) -> CallbackQuery | None:
    """Функция получает количество отелей в выборке: CallbackQuery из amount_hotels().
    Переходит на следующий уровень МС, передает дату заезда в отель."""

    async with state.proxy() as data:
        data["resultsSize"] = int(clb.data)
        logger.info(f'{data["resultsSize"] = }')

    calendar = DetailedTelegramCalendar(
        locale="ru", calendar_id=1, min_date=date.today()
    ).build()[0]

    await clb.message.edit_text(f"Выберите дату заезда:", reply_markup=calendar)

    await ProfileStatesGroup.next()


@logger.catch
async def get_checkOutDate(
    clb: CallbackQuery, state: FSMContext
) -> CallbackQuery | None:
    """Функция получает дату заезда в отель: CallbackQuery из get_checkInDate().
    Переходит на следующий уровень МС, передает дату выезда из отеля."""

    async with state.proxy() as data:
        result = DetailedTelegramCalendar().process(clb.data)[0]
        data["checkInDate"] = result
        logger.info(f'{data["checkInDate"] = }')

    calendar = DetailedTelegramCalendar(
        locale="ru", calendar_id=2, min_date=result + timedelta(days=1)
    ).build()[0]

    await clb.message.edit_text(f"Выберите дату выезда:", reply_markup=calendar)

    await ProfileStatesGroup.next()


@logger.catch
async def ask_is_photos(clb: CallbackQuery, state: FSMContext) -> CallbackQuery | None:
    """Функция получает дату выезда из отеля: CallbackQuery из get_checkOutDate().
    Переходит на следующий уровень МС, передает необходимость фото в конечной выдаче."""

    async with state.proxy() as data:
        result = DetailedTelegramCalendar().process(clb.data)[0]
        data["checkOutDate"] = result
        logger.info(f'{data["checkOutDate"] = }')

    await clb.message.edit_text(
        text="Показать фото отеля?", reply_markup=get_ikb(YESNO_KB)
    )
    await ProfileStatesGroup.next()


@logger.catch
async def amount_photos(clb: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        logger.info(f"is_photo = {bool(clb.data)}")

    await clb.message.edit_text(
        text="Выберите количество фото для отеля.",
        reply_markup=get_ikb(NUM_PHOTOS_KB, 5),
    )
    await ProfileStatesGroup.next()


@logger.catch
async def finish_fsm(clb: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["img_count"] = int(clb.data)
        data["sort"] = "PRICE_LOW_TO_HIGH"
        logger.info(data._data)

    hotels = parse_hotels(**data._data)
    await get_hotels(chat_id=clb.message.chat.id, hotels=hotels)

    await state.finish()


@logger.catch
def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_states, commands="cancel", state="*")
    dp.register_message_handler(get_city, commands="lowprice")
    dp.register_message_handler(get_hotels, commands="test_hotels")  # TODO delete
    dp.register_message_handler(get_location, state=ProfileStatesGroup.get_city)

    dp.register_callback_query_handler(
        amount_hotels, state=ProfileStatesGroup.amount_hotels
    )
    dp.register_callback_query_handler(
        get_checkInDate, state=ProfileStatesGroup.get_checkInDate
    )
    dp.register_callback_query_handler(
        get_checkOutDate, state=ProfileStatesGroup.get_checkOutDate
    )
    dp.register_callback_query_handler(ask_is_photos, state=ProfileStatesGroup.is_photo)
    dp.register_callback_query_handler(
        amount_photos, lambda clb: int(clb.data), state=ProfileStatesGroup.amount_photos
    )
    dp.register_callback_query_handler(
        finish_fsm,
        lambda clb: not int(clb.data),
        state=ProfileStatesGroup.amount_photos,
    )
    dp.register_callback_query_handler(finish_fsm, state=ProfileStatesGroup.fin)


if __name__ == "__main__":
    from create_bot import dp, bot
    from aiogram import executor

    async def on_startup(_):
        await bot.send_message(351886133, "/lowprice")

    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
