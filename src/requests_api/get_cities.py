from requests_api.request import api_request
from loguru import logger


@logger.catch
def parse_cities(city: str) -> dict | None:
    params = {"q": city, "locale": "ru_RU"}

    response = api_request(
        url_endswith='locations/v3/search',
        params=params,
        method='GET'
    )

    cities = None
    try:
        cities = {search.get('regionNames').get('fullName'): search.get('gaiaId')
                  for search in response.get('sr')
                  if search.get('type') == "CITY"}
    except Exception as ex:
        logger.warning(f'response = api_request(): {response}')
        logger.error(ex)
    finally:
        logger.info(f'{cities = }')
        return cities


if __name__ == "__main__":
    cities = parse_cities('рига')
