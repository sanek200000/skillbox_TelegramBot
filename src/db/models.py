from peewee import (
    SqliteDatabase,
    Model,
    PrimaryKeyField,
    CharField,
    DateField,
    ForeignKeyField,
    FloatField,
    IntegerField,
)

# Set DB
db = SqliteDatabase("db.sqlite3")


class BaseModel(Model):
    """Базовый класс для создания таблиц в БД."""

    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = "id"


class User(BaseModel):
    """
    Класс для создания таблицы 'users' в БД.

    Attributes:
        id (int): Уникальный id пользователя.
        name (str): Уникальное имя пользователя (сюда запишется username пользователя Telegram).
    """

    name = CharField(unique=True)

    class Meta:
        db_table = "users"


class History(BaseModel):
    """
    Класс для создания таблицы 'histories' в БД.

    Attributes:
        date (datetime.date): Дата запроса пользователя.
        command (str): Команда запроса ('lowprice', 'highprice', 'bestdeal').
        city (str): Город.
        start_date (datetime.date): Дата заселения в отель.
        end_date (datetime.date): Дата выселения из отеля.
        from_user (str): name - Уникальное имя пользователя из таблицы 'users' для связки таблиц.
    """

    date = DateField()
    command = CharField()
    city = CharField()
    start_date = DateField()
    end_date = DateField()
    from_user = ForeignKeyField(User.name)

    class Meta:
        db_table = "hystories"
        order_by = "date"


class SearchResult(BaseModel):
    """
    Класс для создания таблицы 'results' в БД.

    Attributes:
        hotel_name (str): Название отеля.
        price_per_night (float): Цена за 1 ночь в $.
        total_price (float): Итоговая стоимость за N ночей в $.
        distance_city_center (float): Расстояние до центра города.
        hotel_url (str): url-адрес отеля.
        hotel_area (str): Район расположения отеля.
        amount_nights (int): Количество ночей.
        from_date (datetime.date): date - Уникальная дата запроса из таблицы 'histories' для связки таблиц.
    """

    hotel_name = CharField()
    price_per_night = FloatField()
    total_price = FloatField()
    distance_city_centre = FloatField()
    hotel_area = CharField()
    amount_nights = IntegerField()
    form_date = ForeignKeyField(History.date)

    class Meta:
        db_table = "results"
        order_by = "price_per_night"


if __name__ == "__main__":
    with db:
        db.create_tables([User, History, SearchResult])

    print("DONE")
