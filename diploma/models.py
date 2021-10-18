from peewee import SqliteDatabase, Model, CharField, DateField


db = SqliteDatabase('history.db')


class History(Model):
    """Модель таблицы истории
    запросов пользователя."""
    command = CharField()
    date = DateField()
    hotels = CharField()

    class Meta:
        database = db

    def __enter__(self):
        with db:
            if not self.table_exists():
                self.create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            pass
        except exc_type:
            pass
        finally:
            db.close()
