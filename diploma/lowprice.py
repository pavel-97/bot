from utility import HotelsResponse, check_error_request
from typing import Optional


class LowPrice(HotelsResponse):
    """Класс LowPrice, наследник класса HotelsResponse.
    Класс изменяет поведение класса путем изменения поведения
    метода make_query."""
    @check_error_request
    def make_query(self, count_photo: int = 0, get_photo: bool = True, reverse: bool = False) -> Optional:
        """Метод изменяет поведения при передачи в него аргументов.
        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = False: bool
        """
        return super().make_query(count_photo, get_photo, reverse)
