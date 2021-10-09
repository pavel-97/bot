from utility import HotelsResponse
from typing import Optional


class HighPrice(HotelsResponse):
    """Класс HighPrice, наследник класса HotelsResponse.
    Класс изменяет поведение класса путем изменения поведения
    метода make_query."""
    def make_query(self, count_photo: int = 0, get_photo: bool = True, reverse: bool = True) -> Optional:
        """Метод изменяет поведения при передачи в него аргументов.
        Args:
            count_photo = 0: int
            get_photo = True: bool
            reverse = True: bool
        """
        return super().make_query(count_photo, get_photo, reverse)
