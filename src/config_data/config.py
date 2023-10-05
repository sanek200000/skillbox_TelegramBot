from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


# Tokens
BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')


# Keyboards
START_KB = ('/lowprice', '/highprice', '/bestdeal', '/history', '/kill')
NUM_HOTELS_KB = {str(i): str(i) for i in range(1, 11)}
NUM_PHOTOS_KB = {str(i): str(i) for i in range(1, 6)}
YESNO_KB = {'Да': '1', 'Нет': '0'}

# Other
URL_RAPIDAPI = "https://hotels4.p.rapidapi.com/"
RAPID_HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

if __name__ == "__main__":
    print(f'{BOT_TOKEN = }')
    print(f'{RAPID_API_KEY = }')
    print(f'{START_KB = }')
    print(f'{NUM_HOTELS_KB = }')
    print(f'{NUM_PHOTOS_KB = }')
    print(f'{YESNO_KB = }')
    print(f'{URL_RAPIDAPI = }')
    print(f'{RAPID_HEADERS = }')
