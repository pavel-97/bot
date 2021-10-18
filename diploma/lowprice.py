from utility import HotelsResponse
from typing import Optional


class LowPrice(HotelsResponse):
    """Класс LowPrice, наследник класса HotelsResponse."""
    def make_query(self, query: dict = None, count_photo: int = 0, get_photo: bool = True, reverse: bool = False) -> Optional:
        """Метод изменяет поведения при передачи в него аргументов.
        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = False: bool
        """
        query = {'destinationId': self.make_query_city_id(), 'sortOrder': 'PRICE',
                 'locale': 'en_US', 'currency': 'USD'}
        return super().make_query(query=query, count_photo=count_photo, get_photo=get_photo, reverse=reverse)
