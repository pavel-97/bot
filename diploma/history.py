from models import History


def history(message):
    """Функция открывает содинение с БД,
    Извлекает данные и отправляет их
    пользователю."""
    with History() as table:
        results = []
        for row in table.select():
            row_i = 'Команда: {}; Дата: {}; Отели: {}.'.format(
                row.command,
                row.date,
                row.hotels
            )
            results.append(row_i)
        return '\n'.join(results)
