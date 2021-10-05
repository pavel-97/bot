from telebot.types import Message
from telebot import TeleBot


def help_user(bot: TeleBot, message: Message) -> str:
    """Функция возращает строку с коммандами для бота."""
    return '/help - помощь по командам бота,' \
           '\n/lowprice - вывод самых дешёвых отелей в городе,' \
           '\n/highprice - вывод самых дорогих отелей в городе,' \
           '\n/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра,' \
           '\n/history - вывод истории поиска отелей.'
