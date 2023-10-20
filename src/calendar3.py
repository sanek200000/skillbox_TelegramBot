# pip install aiogram-datepicker --upgrade
# pip uninstall aiogram-datepicker --upgrade

import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor
from config_data.config import BOT_TOKEN

from aiogram_datepicker import Datepicker, DatepickerSettings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, run_tasks_by_default=True)


def _get_datepicker_settings():
    return DatepickerSettings()  # some settings


@dp.message_handler(state='*')
async def _main(message: Message):
    datepicker = Datepicker(_get_datepicker_settings())

    markup = datepicker.start_calendar()
    await message.answer('Select a date: ', reply_markup=markup)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
    datepicker = Datepicker(_get_datepicker_settings())

    date = await datepicker.process(callback_query, callback_data)
    if date:
        await callback_query.message.answer(date.strftime('%d/%m/%Y'))

    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
