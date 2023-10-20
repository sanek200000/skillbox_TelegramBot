from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import get_kb, get_ikb
from requests_api.get_cities import parse_cities
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_data.config import START_KB, NUM_HOTELS_KB, YESNO_KB, NUM_PHOTOS_KB
from loguru import logger
from requests_api.get_hotels import parse_hotels
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta

from handlers.print_result import get_hotels


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
