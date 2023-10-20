from aiogram import executor
from create_bot import dp
from handlers import client, lowprice
from loguru import logger


logger.add(
    "debug.log",
    rotation="10 MB",
    encoding="utf-8",
    level="SUCCESS",
    backtrace=True,
    diagnose=False,
    enqueue=True,
)


async def on_startup(_):
    logger.info("Бот анлин.")


client.register_handlers_client(dp)
lowprice.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
