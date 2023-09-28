from peewee import *

# Set DB
DB = SqliteDatabase('./temp/db.sqlite3')


class BaseModel(Model):
    """Базовый класс для создания таблиц"""

    id = PrimaryKeyField(unique=True)

    class Meta:
        database = DB
        order_by = 'id'


class Profile(BaseModel):
    user_id = CharField(20)
    name = CharField(60)
    photo = CharField(100)
    age = CharField(3)
    description = TextField(200)

    class Meta:
        db_table = 'profiles'

    def __repr__(self) -> str:
        return f"user_id = {self.user_id}"


def delete_profile(user_id):
    Profile.delete().where(Profile.user_id == user_id).execute()
    # try:
    #    user = Profile.get(Profile.user_id == user_id)
    # except DoesNotExist:
    #    print('Сначала создайте пользователя')


def create_profile(user_id, name=None, photo=None, age=None, description=None):
    user = Profile.select().where(Profile.user_id == user_id).count()

    if user:
        Profile.update({Profile.name: name,
                        Profile.photo: photo,
                        Profile.age: age,
                        Profile.description: description}).where(
                            Profile.user_id == user_id).execute()
    else:
        Profile.create(user_id=user_id,
                       name=name,
                       photo=photo,
                       age=age,
                       description=description)


if __name__ == "__main__":
    with DB:
        # DB.drop_tables([Profile], safe=True)
        DB.create_tables([Profile])

    # Profile.insert(user_id='sd').execute()
    create_profile('edsdf2', 'sdfas', 'sdfas', '33', 'sdfas')
    delete_profile('sdf')

    print('DONE')
