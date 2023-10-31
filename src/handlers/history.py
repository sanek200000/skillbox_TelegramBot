from loguru import logger
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_kb import get_kb, get_ikb
from aiogram.types import Message, CallbackQuery
from handlers.print_result import print_hystory

from config_data.config import START_KB

from db.models import *
from datetime import datetime


class ProfileStatesGroup(StatesGroup):
    """Машина состояний"""

    get_date_fsm = State()
    get_search_fsm = State()
    get_search_result_fsm = State()
    finish_fsm = State()


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
async def get_date(msg: Message) -> Message | None:
    """ """

    with db:
        username = User.get(User.name == msg.chat.username)
        get_dates = (
            History.select()
            .where(History.from_user_id == username.id)
            .group_by(History.date)
        )

        dates = {i.date.strftime("%s"): i.date.strftime("%d.%m.%Y") for i in get_dates}
        logger.info(f"{username.id = }\n{dates = }")

    await msg.answer(text="Выберите дату запросов:", reply_markup=get_ikb(dates, 1))
    await ProfileStatesGroup.get_search_fsm.set()


@logger.catch
async def get_search(clb: CallbackQuery) -> Message | None:
    clb_date = datetime.fromtimestamp(int(clb.data))
    clb_user = clb.from_user.username

    with db:
        username = User.get(User.name == clb_user)
        get_records = History.select().where(
            (History.date == clb_date) & (History.from_user_id == username.id)
        )
        records = {
            # record.id: f"город: {record.city}, команда: {record.command}, даты: {record.start_date} - {record.end_date}"
            record.id: f"{record.command}: {record.city} с {record.start_date} по {record.end_date}"
            for record in get_records
        }

        logger.info(f"{records = }")

    await clb.message.edit_text(
        text="Выберите запрос:", reply_markup=get_ikb(records, 1)
    )
    await ProfileStatesGroup.next()


@logger.catch
async def get_search_result(clb: CallbackQuery, state: FSMContext) -> Message | None:
    clb_history_id = int(clb.data)
    clb_chat_id = clb.message.chat.id

    with db:
        get_records = (
            SearchResult.select()
            .where(SearchResult.form_date == clb_history_id)
            .order_by(SearchResult.price_per_night)
        )
        logger.info(f"{get_records = }")

    await print_hystory(records=get_records, chat_id=clb_chat_id)
    await state.finish()


@logger.catch
def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_states, commands="cancel", state="*")
    dp.register_message_handler(get_date, commands="history")
    dp.register_callback_query_handler(
        get_search, state=ProfileStatesGroup.get_search_fsm
    )
    dp.register_callback_query_handler(
        get_search_result, state=ProfileStatesGroup.get_search_result_fsm
    )


if __name__ == "__main__":
    from create_bot import dp, bot
    from aiogram import executor

    async def on_startup(_):
        await bot.send_message(351886133, "/history")

    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
