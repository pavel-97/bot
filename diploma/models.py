from peewee import SqliteDatabase, Model, CharField, DateField, IntegerField


db = SqliteDatabase('history.db')


class History(Model):
    """Модель таблицы истории
    запросов пользователя."""
    command = CharField()
    date = DateField()
    hotels = CharField()
    user_id = IntegerField()

    class Meta:
        database = db
