from requests_api.request import api_request
from loguru import logger


@logger.catch
def get_detail(**kwargs) -> dict:
    hotel_id: str = kwargs.get('hotel_id')
    img_count: int = kwargs.get('img_count')

    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",  # "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = api_request(
        url_endswith='properties/v2/detail',
        params=params,
        method='POST'
    )

    if response and response.get('data'):
        try:
            address = response.get('data').get('propertyInfo').get(
                'summary').get('location').get('address').get('addressLine')
            images_list = response.get('data').get(
                'propertyInfo').get('propertyGallery').get('images')
            images = [image.get('image').get('url') for image in images_list
                      if 'номер' in image.get('accessibilityText').lower()]

            # logger.info(
            #    f'{"; ".join(image.get("accessibilityText").lower() for image in images_list)}')
            logger.info(f'{address = }; {len(images) = }')
            return {'address': address,
                    'images': images[:img_count]}

        except Exception as ex:
            logger.error(ex)
            return {'address': None, 'images': None}
    else:
        return {'address': None, 'images': None}


@logger.catch
def parse_hotels(**kwargs) -> list | None:
    citry_id: str = kwargs.get('citry_id')
    resultsSize: int = kwargs.get('resultsSize')
    sort: str = kwargs.get('sort')
    img_count: int = kwargs.get('img_count')

    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",  # "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": citry_id
        },
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 1,
                "children": []
            }
        ],
        "resultsSize": resultsSize,
        "sort": sort,
        "filters": {
        }
    }

    response = api_request(
        url_endswith='properties/v2/list',
        params=params,
        method='POST'
    )

    try:
        hotels_list = response.get('data').get(
            'propertySearch').get('properties')
        logger.info(f'{len(hotels_list) = }')
    except Exception as ex:
        logger.warning(f'response = api_request(): {response}')
        logger.error(ex)

    try:
        hotels = list()
        for hotel in hotels_list:
            hotel_id = hotel.get('id')
            hotel_name = hotel.get('name')
            price = round(hotel.get('price').get('lead').get('amount'))

            details = get_detail(hotel_id=hotel_id,
                                 img_count=img_count)
            address = details.get('address')
            photos = details.get('images')

            hotels.append({
                'hotel_id': hotel_id,
                'hotel_name': hotel_name,
                'price': price,
                'address': address,
                'photos': photos,
            })

            logger.info(
                f'{len(hotels)}: {hotel_id = }; {hotel_name = }; {price = }; {address = }; {photos = };')
        return hotels
    except Exception as ex:
        logger.error(ex)
        return None


if __name__ == "__main__":
    data = {'citry_id': '3000',
            'resultsSize': 3,
            'sort': "PRICE_LOW_TO_HIGH",
            'img_count': 3}
    hotels = parse_hotels(**data)

    # data = {'hotel_id': '91003653',
    #        'img_count': 3}
    # hotel = get_detail(**data)
    # logger.info(f'{hotel = }')
