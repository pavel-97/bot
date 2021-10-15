from telebot.types import Message
from bot_commands import commands, other_commands
from bot import bot


if __name__ == '__main__':
    @bot.message_handler(content_types=['text'])
    def get_text_message(message: Message) -> None:
        """Функция принимает сообщение от пользователя
        и выполняет действие исходя из запроса пользователя.
        Args:
            message: Message
        """
        if message.text in commands:
            bot.send_message(message.from_user.id, bot(message, commands.get(message.text)))

        elif message.text in other_commands:
            bot.send_message(message.from_user.id, other_commands.get(message.text)(message))

        else:
            bot.send_message(message.from_user.id, 'Комманда не найдена, посмотрите список доступных команд в /help .')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        bot.request['photos'] = call.data
        bot.get_photo(call)

    bot.polling(none_stop=True, interval=0)
