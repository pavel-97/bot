from utility import HotelsResponse


class HighPrice(HotelsResponse):
    """Класс HighPrice, наследник класса HotelsResponse."""
    def make_query(self, query: dict = None, count_photo: int = 0, get_photo: bool = True, reverse: bool = True):
        """Метод изменяет поведения при передачи в него аргументов.
        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = True: bool
        """
        query = {'destinationId': self.request_data.city_id, 'sortOrder': 'PRICE',
                 'checkIn': self.request_data.dates['checkIn'], 'checkOut': self.request_data.dates['checkOut'],
                 'locale': 'en_US', 'currency': 'USD'}
        response = super().make_query(query=query, count_photo=count_photo, get_photo=get_photo, reverse=reverse)
        count_hotels = self.request_data.count_hotels if self.request_data.count_hotels <= len(response) else len(response)
        return response[-int(count_hotels) if reverse else None:int(count_hotels) if not reverse else None]
