from telebot.types import Message


def hello(message: Message) -> str:
    """Функция возращает строку приветствия с пользователем."""
    return 'Привет, {} {}!'.format(
        message.from_user.first_name,
        message.from_user.last_name,
    )
