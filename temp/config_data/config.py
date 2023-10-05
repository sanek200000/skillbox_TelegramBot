from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

HELP_CMD = """
<b>/start</b> - <em>запускает бот</em>
<b>/help</b> - <em>присылает расшифровку команд</em>
<b>/description</b> - <em>описание</em>
<b>/photo</b> - <em>присылает рандомную картинку из списка</em>
<b>/kill</b> - <em>завершить работу бота на сервере</em>
"""

PIC_LIST = [
    'https://main-cdn.sbermegamarket.ru/big1/hlr-system/986/168/469/922/185/5/100029280050b0.jpg',
    'https://www.gastronom.ru/binfiles/images/20220127/ba944b65.jpg',
    'https://www.gastronom.ru/binfiles/images/20141003/m3c0313e.jpg',
    'https://chef.ru/wp-content/uploads/oranges-1117628_1920-1440x1080.jpg',
    'https://www.greeninfo.ru/img/work/article/a_22251_54510.jpg',
]

START_KB = ['/create', '/help', '/kill']
