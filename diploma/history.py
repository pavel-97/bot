from models import History


def history(message):
    """Функция открывает содинение с БД,
    Извлекает данные и отправляет их
    пользователю."""
    results = []
    for row in History.select().where(History.user_id == message.chat.id):
        row_i = 'Команда: {}; Дата: {}; Отели: {}.'.format(
            row.command,
            row.date,
            row.hotels
        )
        results.append(row_i)
    return '\n'.join(results) if results else 'Ваша история пуста'
