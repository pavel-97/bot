from typing import Optional, Any
from telebot.types import Message
from telebot import TeleBot
from utility import get_hotels_data, check_error_request


class Lowprice:
    """Класс Lowprice.
    Args:
        bot
        message
    methods:
        start
        get_city
        get_count
        get_photo
        response
        make_querystring_1
        make_querystring_2
        """
    def __init__(self, bot: TeleBot, message: Message) -> None:
        self.bot = bot
        self.request = dict(city=None, count_hotels=None, photos=None)
        self.start(message)
        self.url_1: str = 'https://hotels4.p.rapidapi.com/locations/search'
        self.url_2: str = 'https://hotels4.p.rapidapi.com/properties/list'
        self.url_3: str = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'

    def __str__(self) -> str:
        return 'Введите название города на аглийском языке'

    def start(self, message: Message) -> None:
        """Метод принимает сообщение от пользователя,
        отправляет сообщение пользователю, ожидает ответ,
        после получения ответа передает управление потоком
        в другую функцию.

        Args:
            message: Message
        """
        self.bot.register_next_step_handler(message, self.get_city)

    def get_city(self, message: Message) -> None:
        """Метод принимает запрос от пользователя,
        который записывается в атрибут класс, задает
        вопрос пользователю и после ответа передает
        поток управления в другую функцию.

        Args:
            message: Message
        """
        self.request['city'] = message.text
        self.bot.send_message(message.from_user.id, 'Введите кол-во отелей')
        self.bot.register_next_step_handler(message, self.get_count)

    def get_count(self, message: Message) -> None:
        """Метод работает аналогично методу self.get_city."""
        self.request['count_hotels'] = message.text
        self.bot.send_message(message.from_user.id, 'Показать фото?(yes/no)')
        self.bot.register_next_step_handler(message, self.get_photo)

    def get_photo(self, message: Message) -> None:
        """Метод работает аналогично методу self.get_city."""
        self.request['photos'] = message.text
        if self.request['photos'] == 'yes':
            self.bot.send_message(message.from_user.id, 'Сколько вы хотите фото?')
            self.bot.register_next_step_handler(message, self.response, True)
        else:
            self.response(message)

    def response(self, message: Message, *args: bool) -> None:
        """Метод отправляет окончательный ответ пользователю
        исходя из его сделанных запросов, в случае неккоректного
        запроса метод отправит сообщение об ошибке.

        Args:
            message: Message
            args: bool
        """
        if self.make_query(int(message.text), *args):
            for i in self.make_query(int(message.text), *args):
                response_i = 'Название: {}\nФото: {}'.format(
                    i.get('name'),
                    '\n'.join(i.get('photos')),
                )
                self.bot.send_message(message.from_user.id, str(response_i))
        else:
            self.bot.send_message(message.from_user.id, 'Вы ввели неправильно данные для запроса.')

    @check_error_request
    def make_query_city_id(self) -> Optional:
        """Метод возращает id города,
        иначе вернет None."""
        query_city_id = {
            'query': self.request['city'],
            'locale': 'en_US',
        }
        return get_hotels_data(
            self.url_1, query_city_id
        ).get('suggestions', {})[0].get('entities', {})[0].get('destinationId')

    @check_error_request
    def make_query(self, count_photo: int = 0, get_photo: bool = False) -> Optional:
        """Метод возращает результат запроса пользователя,
        иначе вернет None.

        Args:
            count_photo: int = 0
            get_photo: bool = False
        """
        query = {'destinationId': self.make_query_city_id(), 'sortOrder': 'PRICE',
                 'locale': 'en_US', 'currency': 'USD'}
        return [
            {'name': hotel['name'],
             'id': hotel['id'],
             'photos': [
                           photo['baseUrl'].format(size='z') for photo in get_hotels_data(self.url_3, {'id': hotel['id']})['hotelImages']
                       ][:count_photo] if get_photo else ['no photo', ],
             } for hotel in get_hotels_data(self.url_2, query)['data']['body']['searchResults']['results']
            if hotel['address']['locality'] == self.request.get('city', '').title()
        ][:int(self.request.get('count_hotels', 0))]
