from restaurant_object import RestaurantObject
from dataclasses import dataclass, replace

class Cook(RestaurantObject):

    def __init__(self):
        self.__info = None
        self.__is_cooking = False

    def set_request(self, request: dataclass):
        food_info = request
        self.__info = food_info
        self.__is_cooking = not self.__is_cooking

    def get_order_info(self) -> tuple:
        return self.__info.table_num, self.__info.customer_num, self.__info.food_num

    def reset_status(self):
        self.__info.items = 0, 0, 0, 0

    @property
    def is_cooking(self):
        return self.__is_cooking

    def get_left_cooking_time(self) -> int:
        return self.__info.cooking_time

    def update(self) -> bool:

        if self.__is_cooking:
            self.__info.cooking_time -= 1
            if self.__info.cooking_time == 0:
                self.__is_cooking = not self.__is_cooking
                return True
        return False
 