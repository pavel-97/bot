import json
import requests
import functools
import os
import re
import logging
from datetime import datetime
from typing import Dict, Callable, Union, List
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument
from telebot import TeleBot
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
from models import History, db


def get_hotels_data(url: str, querystring: Dict) -> Dict:
    """Функция выполняет запрос и
    возвращает словарь с ответом

    Args:
          url: str
          querystring: Dict
    """
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('RapidapiKey'),
    }
    try:
        response = requests.request('GET', url, headers=headers, params=querystring, timeout=10)
        if 199 < int(response.status_code) < 300:
            return json.loads(response.text)
        elif re.findall(r'You have exceeded the MONTHLY quota for Requests on your current plan, BASIC.', json.loads(response.text).get('message')):
            raise requests.exceptions.HTTPError(json.loads(response.text).get('message'))
        else:
            raise requests.exceptions.HTTPError('Ошибка {}'.format(response.status_code))
    except requests.exceptions.ReadTimeout:
        raise requests.exceptions.ReadTimeout('Время ожидания сервера истекло')


def check_error_request(func: Callable) -> Callable:
    """Функция декоратор. Изменяет поведение декорируемой функции,
    есди возникает искючение JSONDecodeError, KeyError."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (json.decoder.JSONDecodeError, KeyError):
            return None
        return result
    return wrapper


def write_history(func: Callable) -> Callable:
    """Функция декоратор. Записывает результат
    декорируемой функции в базу данных."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        command = '/' + args[0].__class__.__name__.lower()
        date = datetime.now().ctime()
        hotels = ', '.join([data['name'] for data in result])
        user_id = args[0].request_data.user_id
        with db:
            History.create(command=command, date=date, hotels=hotels, user_id=user_id)
        return result
    return wrapper


class HotelRequest(TeleBot):
    """Класс HotelRequest. Наследник класс TeleBot.
    Конструктор класс инициализирует экзэмпляры класс."""
    def __init__(self, token) -> None:
        super().__init__(token=token,
                         parse_mode=None, threaded=True,
                         skip_pending=False,
                         num_threads=2,
                         next_step_backend=None,
                         reply_backend=None,
                         exception_handler=None,
                         last_update_id=0,
                         suppress_middleware_excepions=False)
        self.request = None
        self.suggestions = None
        self.calendar = None
        self.callback_data_calendar = CallbackData('None', 'None', 'None', 'None', 'None')
        self.class_name_dict = {
            'LowPrice': ('Введите кол-во отелей', self.get_count),
            'HighPrice': ('Введите кол-во отелей', self.get_count),
            'BestDeal': ('Введите диапозон цен через пробел', self.get_price)
        }

    def __call__(self, message: Message, class_name) -> str:
        """Метод позволяет экземпляру класса вести себя как функция
        и возращаеь строку.
        Args:
            message: Message
            class_name
        """
        self.class_name = class_name
        self.request = User(message.chat.id)
        self.start(message)
        return 'Введите название города'

    def start(self, message: Message) -> None:
        """Метод ожидает ответ от пользователя и
        передает поток управления другому методу.
        Args:
            message: Message
        """
        self.register_next_step_handler(message, self.get_suggestions)

    def get_suggestions(self, message: Message) -> None:
        """Метод запрашивет у API список городо,
        котрые подойдут для пользователя, отправляет инпуты с этими городами
        и ожидает подтверждение выбранного города от пользователя."""
        try:
            self.suggestions = self.class_name.make_suggestions(message)
            keyboard = KeyboardSuggestion(self.suggestions)
            self.send_message(message.chat.id, text='Уточните город' if self.suggestions else 'Уточните правильное название города', reply_markup=keyboard)
        except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError) as err:
            self.send_message(message.chat.id, text=str(err))

    def get_city(self, call) -> None:
        """Метод принимает ответ от пользователя,
        записывает данные в словарь, отправляет сообщение
        пользователю и ожидает ответ, после передает поток
        управления другому методу.
        Args:
            call
        """
        self.request.city_id = call.data
        self.send_message(call.message.chat.id, self.class_name_dict.get(self.class_name.__name__)[0])
        self.register_next_step_handler(call.message, self.class_name_dict.get(self.class_name.__name__)[1])

    def get_price(self, message: Message) -> None:
        """Аналогично методу get_city"""
        try:
            self.request.price_from, self.request.price_to = re.findall(r'\b[\d]+', message.text)
            self.send_message(message.from_user.id, 'Введите расстояние от центра по примеру: 3 миль')
            self.register_next_step_handler(message, self.get_distance)

        except ValueError:
            self.send_message(message.from_user.id, 'Введите два числа через пробел')
            self.register_next_step_handler(message, self.get_price)

    def get_distance(self, message: Message) -> None:
        """Аналогично методу get_city"""
        try:
            self.request.distance_from_center = re.findall(r'\b[\d]+', re.findall(r'\b[\d]+\sмиль', message.text)[0])[0]
            self.request.distance_from_center = int(self.request.distance_from_center)
            self.send_message(message.from_user.id, 'Введите кол-во отелей')
            self.register_next_step_handler(message, self.get_count)
        except (TypeError, IndexError):
            self.send_message(message.from_user.id, 'Введите цифру')
            self.register_next_step_handler(message, self.get_distance)

    def get_count(self, message: Message) -> None:
        """Аналогично методу get_city"""
        if not message.text.isalpha():
            self.request.count_hotels = int(message.text)
            keyboard = KeyboardYesNo()
            self.send_message(message.from_user.id, text='Показать фото? (yes/no)', reply_markup=keyboard)
        else:
            self.send_message(message.from_user.id, 'Введите цифру')
            self.register_next_step_handler(message, self.get_count)

    def get_photo(self, call) -> None:
        """Аналогично методу get_city"""
        self.request.photos = call.data
        if self.request.photos == 'yes':
            self.request.photos = True
            self.send_message(call.message.chat.id, 'Сколько вы хотите фото?')
            self.register_next_step_handler(call.message, self.get_count_photo)
        else:
            self.request.photos = False
            self.get_date(call.message)

    def get_count_photo(self, message: Message) -> None:
        if not message.text.lstrip('/').isalpha():
            self.request.count_photo = message.text if int(message.text) <= 5 else 5
            self.get_date(message)
        else:
            self.send_message(message.chat.id, 'Введите цифру')
            self.register_next_step_handler(message, self.get_count_photo)

    def get_date(self, message: Message, date=datetime.now()) -> None:
        self.calendar = KeyboardCalendar(language=RUSSIAN_LANGUAGE)
        self.callback_data_calendar = CallbackData('calender', 'action', 'year', 'month', 'day')
        dict_text = {
            'checkIn': 'Выберите дату заселения.',
            'checkOut': 'Выберите дату выселения (дата заселения: {}).'.format(
                self.request.dates.get('checkIn')
            ),
        }
        key_text = 'checkOut' if self.request.dates.get('checkIn') is not None else 'checkIn'
        self.send_message(message.chat.id, text=dict_text.get(key_text), reply_markup=self.calendar.create_calendar(
            name=self.callback_data_calendar.prefix,
            year=date.year,
            month=date.month
        ))

    def get_response(self, call) -> None:
        """Метод принимпет ответ от пользователя,
        формирует запрос к API в соответствии с
        требованиями пользователя, получает ответ и
        отправляет его пользователю.
        Args:
            call
        """
        try:
            with self.class_name(request_data=self.request) as response:
                for response_i, photos_i in response(count_photo=int(self.request.count_photo), get_photo=self.request.photos):
                    self.send_message(call.message.chat.id, response_i)
                    if photos_i:
                        self.send_media_group(chat_id=call.message.chat.id, media=photos_i)
        except (StopIteration, requests.exceptions.ReadTimeout, requests.exceptions.HTTPError) as err:
            logging.exception('{}'.format(

                datetime.now().strftime('%Y-$m-%d %H:%M:%S')
            ), exc_info=True)
            self.send_message(call.message.chat.id, str(err))


class HotelsResponse:
    """Класс HotelsResponse. Конструктор
    класса принимает словарь с параметрами
    запроса от пользователя.
    Args:
        request_data: Dict
    """
    url_1: str = 'https://hotels4.p.rapidapi.com/locations/search'
    url_2: str = 'https://hotels4.p.rapidapi.com/properties/list'
    url_3: str = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'

    def __init__(self, request_data: 'User') -> None:
        self.request_data = request_data

    def __call__(self, count_photo: int, get_photo: bool) -> List[List[Union[str, List[InputMediaDocument], None]]]:
        """Метод принимает сообщение от пользователя,
        делает запрос к API и возращает ответ.
        Args:
            get_photo=False: bool
        """
        response = self.make_query(count_photo=count_photo, get_photo=get_photo)
        if response:
            data_response = []
            for data in response:
                response_i = 'Название: {}.\nАдрес: {}.\nРасстояние от центра: {}\nЦена: {}'.format(
                    data.get('name'),
                    data.get('address'),
                    data.get('distance_from_center'),
                    data.get('price'),
                )
                photos = [InputMediaDocument(media=link) for link in data.get('photos')] if get_photo else None
                data_response.append([str(response_i), photos])
            return data_response
        else:
            raise StopIteration('Вы ввели неправильно данные для запроса.')

    def __enter__(self) -> 'HotelsResponse':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is StopIteration:
            raise exc_val

    @check_error_request
    @write_history
    def make_query(self, query: dict = None, count_photo: int = 0, get_photo: bool = True, reverse: bool = False) -> List[Dict[str, Union[str, list[str]]]]:
        """Метод возращает результат запроса пользователя.

        Args:
            query: dict = None
            count_photo: int = 0
            get_photo: bool = False
            reverse: bool = False
        """
        response = get_hotels_data(self.url_2, query)['data']['body']['searchResults']['results']
        return [
                   {'name': hotel['name'],
                    'id': hotel['id'],
                    'address': hotel['address'].get('streetAddress'),
                    'distance_from_center': hotel['landmarks'][0]['distance'],
                    'price': hotel['ratePlan']['price']['current'],
                    'photos': [photo['baseUrl'].format(size='z')
                               for photo in get_hotels_data(self.url_3, {'id': hotel['id']})
                                    ['hotelImages']
                               ]
                    [:count_photo] if get_photo else ['no photo', ],
                    }
                   for hotel in response
            ]

    @classmethod
    @check_error_request
    def make_suggestions(cls, message: Message) -> Dict[str, str]:
        """Метод класса. Возращает список
        для пользователя."""
        cls.url_1 = "https://hotels4.p.rapidapi.com/locations/search"
        query = {
            'query': message.text,
            'locale': 'ru_RU',
        }
        request = get_hotels_data(cls.url_1, query).get('suggestions')
        response = {name['destinationId']: name['name'] for suggestion in request for name in suggestion['entities']} \
            if request\
            else {}
        return response


class User:
    def __init__(self, telegram_id: int) -> None:
        self.city_id = None
        self.count_hotels = 0
        self.photos = False
        self.count_photo = 0
        self.price_from = 'None'
        self.price_to = 'None'
        self.distance_from_center = '0'
        self.user_id = telegram_id
        self.dates = {'checkIn': None, 'checkOut': None}

    def __str__(self):
        return self.user_id


class KeyboardSuggestion(InlineKeyboardMarkup):
    def __init__(self, cities_data: dict) -> None:
        super().__init__()
        for id_city in cities_data:
            self.add(InlineKeyboardButton(text=cities_data.get(id_city, 'None'), callback_data=str(
                {'data': id_city, 'method': 'get_city'}
            ).replace("'", '"')))


class KeyboardYesNo(InlineKeyboardMarkup):
    """Класс KeyboardYesNo. Наследник InlineKeyboardMarkup
    Предоставляет готовую клавиатуру для пользователя."""
    def __init__(self):
        super().__init__()
        self.add(InlineKeyboardButton(text='yes', callback_data=str(
            {'data': 'yes', 'method': 'get_photo'}
        ).replace("'", '"')))
        self.add(InlineKeyboardButton(text='no', callback_data=str(
            {'data': 'no', 'method': 'get_photo'}
        ).replace("'", '"')))


class KeyboardCalendar(Calendar):
    def __init__(self, language):
        super().__init__(language=language)
