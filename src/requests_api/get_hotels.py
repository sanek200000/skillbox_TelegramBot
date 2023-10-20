from requests_api.request import api_request
from loguru import logger
import datetime


@logger.catch
def get_detail(**kwargs) -> dict:
    """
    Функция получает словарь с id отеля (hotel_id) и количеством фото (img_count).
    Делает запрос на получение детальных данных по отелю.
    Возвращает словарь с адресом и фотографиями отеля.
    Если что-то пошло не так, то вернется словарь с пустыми значениями.
    """
    hotel_id: str = kwargs.get("hotel_id")
    img_count: int = kwargs.get("img_count")

    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",  # "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id,
    }
    logger.info(f"get_detail {params = }")

    response = api_request(
        url_endswith="properties/v2/detail", params=params, method="POST"
    )

    if response and response.get("data"):
        try:
            address = (
                response.get("data")
                .get("propertyInfo")
                .get("summary")
                .get("location")
                .get("address")
                .get("addressLine")
            )
            images_list = (
                response.get("data")
                .get("propertyInfo")
                .get("propertyGallery")
                .get("images")
            )
            images = [
                image.get("image").get("url")
                for image in images_list
                if (
                    "фасад" in image.get("accessibilityText").lower()
                    or "номер" in image.get("accessibilityText").lower()
                )
            ]
            # logger.info(
            #    [image.get("accessibilityText").lower() for image in images_list]
            # )

            return {"address": address, "images": images[:img_count]}
        except Exception as ex:
            logger.error(ex)
            return {"address": None, "images": None}
    else:
        return {"address": None, "images": None}


@logger.catch
def parse_hotels(**kwargs) -> list | None:
    city_id: str = kwargs.get("city_id")
    resultsSize: int = kwargs.get("resultsSize")
    sort: str = kwargs.get("sort")
    img_count: int = kwargs.get("img_count")
    checkInDate: datetime = kwargs.get("checkInDate")
    checkOutDate: datetime = kwargs.get("checkOutDate")
    timedelta: datetime = checkOutDate - checkInDate

    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",  # "en_US",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": checkInDate.day,
            "month": checkInDate.month,
            "year": checkInDate.year,
        },
        "checkOutDate": {
            "day": checkOutDate.day,
            "month": checkOutDate.month,
            "year": checkOutDate.year,
        },
        "rooms": [{"adults": 1, "children": []}],
        "resultsSize": resultsSize,
        "sort": sort,
        "filters": {},
    }
    logger.info(f"parse_hotels {params = }")

    response = api_request(
        url_endswith="properties/v2/list", params=params, method="POST"
    )

    try:
        hotels_list = response.get("data").get("propertySearch").get("properties")
        logger.info(f"{len(hotels_list) = }")
    except Exception as ex:
        logger.warning(f"response = api_request(): {response}")
        logger.error(ex)

    try:
        hotels = list()
        for hotel in hotels_list:
            hotel_id = hotel.get("id")
            hotel_name = hotel.get("name")
            price = round(hotel.get("price").get("lead").get("amount"))
            destinationInfo = (
                hotel.get("destinationInfo").get("distanceFromDestination").get("value")
            )

            details = get_detail(hotel_id=hotel_id, img_count=img_count)
            logger.info(f"get_detail() return: {details}")

            address = details.get("address")
            photos = details.get("images")

            hotels.append(
                {
                    "hotel_id": hotel_id,
                    "hotel_name": hotel_name,
                    "price": price,
                    "checkInDate": datetime.date.strftime(checkInDate, r"%d-%m-%Y"),
                    "checkOutDate": datetime.date.strftime(checkOutDate, r"%d-%m-%Y"),
                    "timedelta": timedelta.days,
                    "address": address,
                    "destinationInfo": destinationInfo,
                    "photos": photos,
                }
            )

            logger.info(
                "\n".join(
                    [
                        "",
                        f"{len(hotels)}: {hotel_id = }",
                        f"{hotel_name = }",
                        f"{price = }",
                        f"{checkInDate = }",
                        f"{checkOutDate = }",
                        f"{timedelta = }",
                        f"{address = }",
                        f"{destinationInfo = }",
                        f"{photos = }",
                        "\n",
                    ]
                )
            )

        return hotels
    except Exception as ex:
        logger.error(ex)
        return None


if __name__ == "__main__":
    data = {
        "citry_id": "3000",
        "resultsSize": 3,
        "sort": "PRICE_LOW_TO_HIGH",
        "img_count": 5,
        "checkInDate": datetime.date(2023, 10, 10),
        "checkOutDate": datetime.date(2023, 10, 12),
    }

    hotels = parse_hotels(**data)
    logger.info(hotels)

    # data = {'hotel_id': '91003653',
    #        'img_count': 3}
    # hotel = get_detail(**data)
    # logger.info(f'{hotel = }')
