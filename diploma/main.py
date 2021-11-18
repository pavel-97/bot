import datetime
import json
from dateutil import relativedelta
from telebot.types import Message
from bot_commands import commands, other_commands
from loader import bot
from loguru import logger


@bot.message_handler(content_types=['text'])
@logger.catch
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


@bot.callback_query_handler(func=lambda call: call.data.startswith(bot.callback_data_calendar.prefix))
@logger.catch
def callback_calendar(call):
    name, action, year, month, day = call.data.split(bot.callback_data_calendar.sep)

    if action == 'DAY':
        day_start = bot.request.dates['checkIn']
        date = [int(year), int(month), int(day)]
        bot.request.dates['checkIn' if day_start is None else 'checkOut'] = datetime.date(*date).strftime('%Y-%m-%d')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if not bot.request.dates.get('checkOut'):
            bot.get_date(call.message)

    elif action == 'NEXT-MONTH':
        date = datetime.date(year=int(year), month=int(month), day=1) + relativedelta.relativedelta(months=1)
        bot.get_date(call.message, date)

    elif action == 'PREVIOUS-MONTH':
        date = datetime.date(year=int(year), month=int(month), day=1) - relativedelta.relativedelta(months=1)
        bot.get_date(call.message, date)

    elif action == 'CANCEL':
        bot.send_message(call.message.chat.id, 'Комманда не найдена, посмотрите список доступных команд в /help .')

    if all(bot.request.dates.values()):
        bot.get_response(call)


@bot.callback_query_handler(func=lambda call: True)
@logger.catch
def callback_worker(call):
    """Функция принимает событие
    при нажатии на кнопку формы, извлекает
    данные и отправляет их другой функции."""
    try:
        name_method = json.loads(call.data).get('method')
        call.data = json.loads(call.data).get('data')
        bot.__getattribute__(name_method)(call)
    except (json.JSONDecodeError, AttributeError):
        bot.send_message(call.message.chat.id, text='Комманда не найдена, посмотрите список доступных команд в /help .')


bot.polling(none_stop=True, interval=3)
