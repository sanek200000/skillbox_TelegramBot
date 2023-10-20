# pip install python-telegram-bot-calendar
# pip uninstall python-telegram-bot-calendar

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from aiogram import Bot, Dispatcher, executor
from config_data.config import BOT_TOKEN
from datetime import date

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message):
    calendar, step = DetailedTelegramCalendar(
        locale="ru", calendar_id=1, min_date=date.today()
    ).build()

    await bot.send_message(
        message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar
    )


@dp.callback_query_handler(DetailedTelegramCalendar.func(calendar_id=1))
async def inline_kb_answer_callback_handler(query):
    print(f"{query.data = }")

    result, key, step = DetailedTelegramCalendar().process(query.data)

    if not result and key:
        await bot.edit_message_text(
            f"Select {LSTEP[step]}",
            query.message.chat.id,
            query.message.message_id,
            reply_markup=key,
        )
    elif result:
        await bot.edit_message_text(
            f"You selected {result}", query.message.chat.id, query.message.message_id
        )


executor.start_polling(dp, skip_updates=True)
