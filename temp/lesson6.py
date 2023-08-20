from aiogram import Bot, Dispatcher, types, executor
from config_data.config import *


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

HELP_CMD = """
<b>/give</b> - <em>присылает стикер</em>
<b>/help</b> - <em>присылает расшифровку команд</em>"""


async def on_startup(_):    # readme p.5
    print('Я запустился!')


@dp.message_handler(commands=['give'])  # readme p.1
async def give_cmd(message: types.Message):
    await message.answer('Смотри какой смишной Чебурашка ❤️')
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEKEAZk36FCJ4UyrjNIxJenCzJMw-4B-wACewADwZxgDNsaH7YdVDaIMAQ')


@dp.message_handler(commands=['help'])  # readme p.4
async def help_cmd(message: types.Message):
    await message.answer(text=HELP_CMD, parse_mode='HTML')


@dp.message_handler(content_types=['sticker'])  # readme p.6
async def get_sticker_id_cmd(message: types.Message):
    await message.answer(f'ID стикера:\n{message.sticker.file_id}')


@dp.message_handler()
async def heart_cmd(message: types.Message):
    if message.text == '❤️':
        await message.answer('🖤')  # readme p.2
    elif '✅' in message.text:
        count = message.text.count('✅')
        await message.answer(
            f'Количество ✅ в сообщении равно {count}')    # readme p.3


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
