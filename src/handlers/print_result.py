from loguru import logger
from create_bot import bot
from keyboards.client_kb import get_kb
from config_data.config import START_KB
from db.save_search import save_search_result
from aiogram.types import Message, InputMediaPhoto
from requests_api.get_hotels import parse_hotels


@logger.catch
async def print_hystory(records: dict, chat_id: int) -> Message | None:
    for record in records:
        amount_nights = record.amount_nights
        price_per_night = record.price_per_night
        fullprice = amount_nights * price_per_night

        about_hotel = "\n".join(
            [
                f"Отель: {record.hotel_name}",
                f"Адрес: {record.hotel_area}",
                f"Удаленность от центра: {record.distance_city_centre} км.",
                f"Количество ночей: {amount_nights}",
                f"Цена за ночь: ${price_per_night}",
                f"Полная стоимость: ${fullprice}",
            ]
        )

        await bot.send_message(chat_id=chat_id, text=about_hotel)

    msg = await bot.send_message(
        chat_id=chat_id, text="ass", reply_markup=get_kb(START_KB, 2)
    )
    await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)


@logger.catch
async def print_hotels(search_result) -> Message | None:
    print(f"{search_result = }")  # TODO delete this
    chat_id = search_result.get("chat_id")

    hotels_to_db_list = list()
    hotels = parse_hotels(**search_result)
    for hotel in hotels:
        hotel_name = hotel.get("hotel_name")
        address = hotel.get("address")
        price = hotel.get("price")
        days = hotel.get("timedelta")
        destinationInfo = hotel.get("destinationInfo")
        checkInDate = hotel.get("checkInDate")
        checkOutDate = hotel.get("checkOutDate")

        try:
            fullprice = "{:.2f}".format(float(price) * int(days))
        except Exception as ex:
            fullprice = None
            logger.error(f"{ex} \n{price = } \n{days = }")

        about_hotel = "\n".join(
            [
                f"Отель: {hotel_name}",
                f"Адрес: {address}",
                f"Удаленность от центра: {destinationInfo} км.",
                f"Дата заезда: {checkInDate}",
                f"Дата выезда: {checkOutDate}",
                f"Цена за ночь: ${price}",
                f"Полная стоимость: ${fullprice}",
            ]
        )
        await bot.send_message(chat_id=chat_id, text=about_hotel)

        images = hotel.get("photos")
        if images:
            photos_media_list = [InputMediaPhoto(media=photo) for photo in images]
            logger.info(f"{photos_media_list = }")

            await bot.send_media_group(chat_id=chat_id, media=photos_media_list)
        else:
            await bot.send_message(chat_id=chat_id, text="NO PHOTOS")

        hotels_to_db_list.append(
            {
                "hotel_name": hotel_name,
                "price_per_night": price,
                "total_price": fullprice,
                "distance_city_centre": destinationInfo,
                # "hotel_url": address,
                "hotel_area": address,
                "amount_nights": days,
                # "form_date": history,
            }
        )
    print(f"{hotels_to_db_list = }")
    save_search_result(for_history=search_result, for_hotels=hotels_to_db_list)


if __name__ == "__main__":
    import datetime
    from create_bot import dp, bot
    from aiogram import executor

    search_result = {
        "command": "/lowprice",
        "sort": "PRICE_LOW_TO_HIGH",
        "date": "2023-10-24 19:48:40",
        "from_user": "heist2000",
        "cities": {
            "3000": "Рига, Латвия",
            "3000442633": "Рига, Мичиган, США",
            "181962": "Риго, Квебек, Канада",
            "553248635077639743": "Рига, Нью-Йорк, США",
        },
        "city_id": "3000",
        "city": "Рига, Латвия",
        "resultsSize": 1,
        "checkInDate": datetime.date(2023, 10, 24),
        "checkOutDate": datetime.date(2023, 10, 31),
        "img_count": 0,
        "chat_id": 351886133,
    }

    print_hotels(search_result)

    async def on_startup(_):
        await bot.send_message(351886133, "/lowprice")

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
