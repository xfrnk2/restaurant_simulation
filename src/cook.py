from dataclasses import dataclass


class Cook:

    def __init__(self, request: dataclass):
        self.__info = request
        self.__cooking_time = request.cooking_time

    @property
    def order_info(self) -> dataclass:
        return self.__info

    def get_left_cooking_time(self) -> int:
        return self.__info.cooking_time

    def update(self) -> bool:

        self.__cooking_time -= 1
        if self.__cooking_time == 0:
            return True
        return False
