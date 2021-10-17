from utility import HotelsResponse, check_error_request
from typing import Optional


class HighPrice(HotelsResponse):
    """Класс HighPrice, наследник класса HotelsResponse."""
    @check_error_request
    def make_query(self, count_photo: int = 0, get_photo: bool = True, reverse: bool = True) -> Optional:
        """Метод изменяет поведения при передачи в него аргументов.
        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = True: bool
        """
        query = {'destinationId': self.make_query_city_id(), 'sortOrder': 'PRICE',
                 'locale': 'en_US', 'currency': 'USD'}
        return super().make_query(query=query, count_photo=count_photo, get_photo=get_photo, reverse=reverse)
