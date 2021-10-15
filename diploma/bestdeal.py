from typing import Optional, Callable
from utility import HotelsResponse, get_hotels_data, check_error_request


def filter_count(func: Callable) -> Callable:
    """Функция декоратор filter_count.
    Фильтрует результат декорируемой функции."""
    def wrapper(*args, **kwargs) -> Optional:
        result = func(*args, **kwargs)[:args[0].request_data['count_hotels']]
        return result
    return wrapper


def filter_distance(func: Callable) -> Callable:
    """Аналогично filter_count"""
    def wrapper(*args, **kwargs) -> Optional:
        result = filter(lambda elem: float(elem['distance_from_center'].rstrip(' miles')) < int(args[0].request_data['distance_from_center']), func(*args, **kwargs))
        return list(result) if result is not None else None
    return wrapper


def filter_price(func: Callable) -> Callable:
    """Аналогично filter_count"""
    def wrapper(*args, **kwargs) -> Optional:
        result = filter(lambda elem: int(args[0].request_data['price_from']) < int(elem['price'].lstrip('$')) < int(args[0].request_data['price_to']), func(*args, **kwargs))
        return list(result) if result is not None else None
    return wrapper


class BestDeal(HotelsResponse):
    """Класс BestDeal, наследник класса HotelsResponse.
    Класс изменяет поведение класса путем изменения поведения
    метода make_query."""
    @check_error_request
    @filter_count
    @filter_distance
    @filter_price
    def make_query(self, count_photo: int = 0, get_photo: bool = True) -> Optional:
        """Метод make_query переопределен. Изменяет свое
        поведение путем применением декораторов.

        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = False: bool
        """
        query = {'destinationId': self.make_query_city_id(), 'sortOrder': 'PRICE',
                 'locale': 'en_US', 'currency': 'USD'}

        return [
            {
                'name': hotel['name'],
                'id': hotel['id'],
                'address': hotel['address']['streetAddress'],
                'distance_from_center': hotel['landmarks'][0]['distance'],
                'price': hotel['ratePlan']['price']['current'],
                'photos': [
                              photo['baseUrl'].format(size='z') for photo in get_hotels_data(self.url_3, {'id': hotel['id']})['hotelImages']
                          ][:count_photo] if get_photo else ['no_photo', ],
            } for hotel in get_hotels_data(self.url_2, querystring=query)['data']['body']['searchResults']['results']
            if hotel['address']['locality'] == self.request_data.get('city', '').title()
        ]

