import json
import requests
from typing import Dict, Callable


def get_hotels_data(url: str, querystring: Dict) -> Dict:
    """Функция выполняет запрос и
    возвращает словарь с ответом

    Args:
          url: str
          querystring: Dict
    """
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "56758a6b2amsh4e4f82ef95854c3p1d0363jsna1cd255dcf51"
        }
    response = requests.request('GET', url, headers=headers, params=querystring)
    return json.loads(response.text)


def check_error_request(func: Callable) -> Callable:
    """Функция декоратор. Изменяет поведение декорируемой функции,
    есди возникает искючение KeyError."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            return None
        return result
    return wrapper
