from loguru import logger
from create_bot import bot
from aiogram.types import Message, InputMediaPhoto


@logger.catch
async def get_hotels(chat_id: Message, hotels: dict) -> Message | None:
    for hotel in hotels:
        price = hotel.get("price")
        days = hotel.get("timedelta")

        try:
            fullprice = "{:.2f}".format(float(price) * int(days))
        except Exception as ex:
            logger.error(f"{ex} \n{price = } \n{days = }")
            fullprice = None

        about_hotel = "\n".join(
            [
                f'Отель: {hotel.get("hotel_name")}',
                f'Адрес: {hotel.get("address")}',
                f'Удаленность от центра: {hotel.get("destinationInfo")} км.',
                f'Дата заезда: {hotel.get("checkInDate")}',
                f'Дата выезда: {hotel.get("checkOutDate")}',
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
