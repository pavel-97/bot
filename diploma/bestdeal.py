from utility import HotelsResponse


class BestDeal(HotelsResponse):
    """Класс BestDeal, наследник класса HotelsResponse.
    Класс изменяет поведение класса путем изменения поведения
    метода make_query."""
    def make_query(self, query: dict = None, count_photo: int = 0, get_photo: bool = True, reverse: bool = False):
        """Метод make_query.

        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = False: bool
        """
        query = {'destinationId': self.request_data.city_id, 'sortOrder': 'DISTANCE_FROM_LANDMARK',
                 'landmarkIds': 'City center', 'locale': 'en_US', 'currency': 'USD',
                 'checkIn': self.request_data.dates['checkIn'], 'checkOut': self.request_data.dates['checkOut'],
                 'priceMin': self.request_data.price_from, 'priceMax': self.request_data.price_to}
        response = super().make_query(query=query, count_photo=count_photo, get_photo=get_photo)
        count_filtered_hotels = len(
            list(
                filter(
                    lambda elem: float(elem['distance_from_center'].split()[0]) <= self.request_data.distance_from_center, response
                )
            )
        )
        count_hotels = self.request_data.count_hotels if self.request_data.count_hotels <= count_filtered_hotels else count_filtered_hotels
        return list(
            filter(lambda elem: float(elem['distance_from_center'].split()[0]) <= self.request_data.distance_from_center, response)
        )[:count_hotels]
