from db.models import *
from loguru import logger


@logger.catch
def save_search_result(for_history: dict, for_hotels: list) -> None:
    with db:
        try:
            username = User.create(name=for_history.get("from_user"))
        except:
            username = User.get(User.name == for_history.get("from_user"))
        logger.info(f"{username = }")

        history = History.create(
            date=for_history.get("date"),
            command=for_history.get("command"),
            city=for_history.get("city"),
            start_date=for_history.get("checkInDate"),
            end_date=for_history.get("checkOutDate"),
            from_user=username.id,
        )

        for hotel in for_hotels:
            hotel["form_date"] = history.id

        SearchResult.insert_many(for_hotels).execute()


if __name__ == "__main__":
    with db:
        username = User.get(User.name == "qqq")
        print(username.id)
