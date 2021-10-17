from typing import Optional
from utility import HotelsResponse, check_error_request


class BestDeal(HotelsResponse):
    """Класс BestDeal, наследник класса HotelsResponse.
    Класс изменяет поведение класса путем изменения поведения
    метода make_query."""
    @check_error_request
    def make_query(self, count_photo: int = 0, get_photo: bool = True) -> Optional:
        """Метод make_query.

        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = False: bool
        """
        query = {'destinationId': self.make_query_city_id(), 'sortOrder': 'DISTANCE_FROM_LANDMARK',
                 'landmarkIds': 'City center', 'locale': 'en_US', 'currency': 'USD',
                 'priceMin': self.request_data['price_from'], 'priceMax': self.request_data['price_to']}
        return super().make_query(query=query, count_photo=count_photo, get_photo=get_photo)
