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
<b>/give</b> - <em>присылает стикер</em>
"""
