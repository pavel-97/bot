from models import History


def history(message):
    """Функция открывает содинение с БД,
    Извлекает данные и отправляет их
    пользователю."""
    results = []
    list_history = History.select().where(History.user_id == message.chat.id)
    for row in list_history[None if len(list_history) <= 5 else -5:]:
        row_i = 'Команда: {}; Дата: {}; Отели: {}.\n'.format(
            row.command,
            row.date,
            row.hotels
        )
        results.append(row_i)
    return '\n'.join(results) if results else 'Ваша история пуста'
