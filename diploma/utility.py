import json
import requests
from typing import Dict, Callable, Optional, Union, List
import functools
from telebot.types import Message
from telebot import TeleBot
import os


def get_hotels_data(url: str, querystring: Dict) -> Dict:
    """Функция выполняет запрос и
    возвращает словарь с ответом

    Args:
          url: str
          querystring: Dict
    """
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "e76b542448msh855d062b981342bp1d6e4bjsne657ae458330"
        }
    response = requests.request('GET', url, headers=headers, params=querystring)
    return json.loads(response.text)


def check_error_request(func: Callable) -> Callable:
    """Функция декоратор. Изменяет поведение декорируемой функции,
    есди возникает искючение KeyError."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            return None
        return result
    return wrapper


class HotelRequest(TeleBot):
    """Класс HotelRequest. Наследник класс TeleBot.
    Конструктор класс инициализирует экзэмпляры класс."""
    def __init__(self) -> None:

        super().__init__(token=os.environ.get('TOKEN'),
                         parse_mode=None, threaded=True,
                         skip_pending=False,
                         num_threads=2,
                         next_step_backend=None,
                         reply_backend=None,
                         exception_handler=None,
                         last_update_id=0,
                         suppress_middleware_excepions=False)
        self.request = dict(city=None, count_hotels=None, photos=None)

    def __call__(self, message: Message, class_name) -> str:
        """Метод позволяет экземпляру класса вести себя как функция
        и возращаеь строку.
        Args:
            message: Message
            class_name
        """
        self.class_name = class_name
        self.start(message)
        return 'Введите название города на аглийском языке'

    def start(self, message: Message) -> None:
        """Метод ожидает ответ от пользователя и
        передает поток управления другому методу.
        Args:
            message: Message
        """
        self.register_next_step_handler(message, self.get_city)

    def get_city(self, message: Message) -> None:
        """Метод принимает ответ от пользователя,
        записывает данные в словарь, отправляет сообщение
        пользователю и ожидает ответ, после передает поток
        управления другому методу.
        Args:
            message: Message
        """
        self.request['city'] = message.text
        self.send_message(message.from_user.id, 'Введите кол-во отелей')
        self.register_next_step_handler(message, self.get_count)

    def get_count(self, message: Message) -> None:
        """Аналогично методу get_city"""
        self.request['count_hotels'] = message.text
        self.send_message(message.from_user.id, 'Показать фото? (yes/no)')
        self.register_next_step_handler(message, self.get_photo)

    def get_photo(self, message: Message) -> None:
        """Аналогично методу get_city"""
        self.request['photo'] = message.text
        if self.request['photo'] == 'yes':
            self.send_message(message.from_user.id, 'Сколько вы хотите фото?')
            self.register_next_step_handler(message, self.response)
        else:
            self.register_next_step_handler(message, self.response)

    def response(self, message: Message) -> None:
        """Метод принимпет ответ от пользователя,
        формирует запрос к API в соответствии с
        требованиями пользователя, получает ответ и
        отправляет его пользователю.
        Args:
            message: Message
        """
        response = self.class_name(request_data=self.request)
        for response_i in response(message, get_photo=True):
            self.send_message(message.from_user.id, response_i)


class HotelsResponse:
    """Класс HotelsResponse. Конструктор
    класса принимает словарь с параметрами
    запроса от пользователя.
    Args:
        request_data: Dict
    """
    def __init__(self, request_data: Dict) -> None:
        self.request_data = request_data
        self.url_1: str = 'https://hotels4.p.rapidapi.com/locations/search'
        self.url_2: str = 'https://hotels4.p.rapidapi.com/properties/list'
        self.url_3: str = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'

    def __call__(self, message: Message, get_photo: bool = False) -> Union[List, str]:
        """Метод принимает сообщение от пользователя,
        делает запрос к API и возращает ответ.
        Args:
            message: Message
            get_photo=False: bool
        """
        if self.make_query(int(message.text), get_photo):
            response = []
            for i in self.make_query(int(message.text), get_photo):
                response_i = 'Название: {}\nФото: {}'.format(
                    i.get('name'),
                    '\n'.join(i.get('photos')),
                )
                response.append(str(response_i))
            return response
        else:
            return 'Вы ввели неправильно данные для запроса.'

    def make_query_city_id(self) -> Optional:
        """Метод возращает id города,
        иначе вернет None."""
        query_city_id = {
            'query': self.request_data['city'],
            'locale': 'en_US',
        }
        return get_hotels_data(
            self.url_1, query_city_id
        ).get('suggestions', {})[0].get('entities', {})[0].get('destinationId')

    @check_error_request
    def make_query(self, count_photo: int = 0, get_photo: bool = True, reverse: bool = False) -> Optional:
        """Метод возращает результат запроса пользователя,
        иначе вернет None.

        Args:
            count_photo: int = 0
            get_photo: bool = False
            reverse: bool = False
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
            if hotel['address']['locality'] == self.request_data.get('city', '').title()
        ][-int(self.request_data.get('count_hotels', 0)) if reverse else None:int(self.request_data.get('count_hotels', 0)) if not reverse else None]
