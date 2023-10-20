import requests
from config_data.config import RAPID_HEADERS, URL_RAPIDAPI
from loguru import logger


@logger.catch
def get_request(url, params):
    try:
        response = requests.get(
            url=url, headers=RAPID_HEADERS, params=params, timeout=10
        )
        if response.status_code == requests.codes.ok:
            return response.json()
        return None
    except Exception as ex:
        logger.error(ex)
        return None
    finally:
        logger.info(f"{response.status_code = }")


@logger.catch
def post_request(url, params):
    try:
        response = requests.post(
            url=url, headers=RAPID_HEADERS, json=params, timeout=10
        )
        if response.status_code == requests.codes.ok:
            return response.json()
        return None
    except Exception as ex:
        logger.error(ex)
        return None
    finally:
        logger.info(f"{response.status_code = }")


@logger.catch
def api_request(url_endswith: str, params: dict, method: str) -> dict:
    url = URL_RAPIDAPI + url_endswith

    if method == "GET":
        return get_request(url, params)
    else:
        return post_request(url, params)


if __name__ == "__main__":
    searches = api_request(
        url_endswith="locations/v3/search",
        params={"q": "париж", "locale": "ru_RU"},
        method="GET",
    )

    cities = dict()
    if searches and searches.get("sr"):
        for search in searches.get("sr"):
            if search.get("type") == "CITY":
                city_id = search.get("gaiaId")
                region = search.get("regionNames").get("fullName")
                cities[region] = city_id
    logger.info(f"{cities = }")
