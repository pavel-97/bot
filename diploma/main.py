from bot import bot
from telebot.types import Message
from bot_commands import commands


if __name__ == '__main__':
    @bot.message_handler(content_types=['text'])
    def get_text_message(message: Message) -> None:
        """Функция принимает сообщение от пользователя
        и выполняет действие исходя из запроса пользователя.
        Args:
            message: Message
        """
        if message.text in commands:
            bot.send_message(message.from_user.id, commands.get(message.text)(bot, message))
        else:
            bot.send_message(message.from_user.id, 'Комманда не найдена, посмотрите список доступных команд в /help .')


    bot.polling(none_stop=True, interval=0)
