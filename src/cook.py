from restaurant_object import RestaurantObject


class Cook(RestaurantObject):

    def __init__(self):
        self.__food_number = 0
        self.__cooking_time = 0
        self.__customer_number = 0
        self.__table_number = 0
        self.__is_cooking = False

    def set_request(self, request: tuple):
        self.__table_number, self.__customer_number, \
             self.__food_number, self.__cooking_time = request

        self.__is_cooking = not self.__is_cooking

    def get_order_info(self) -> tuple:
        return self.__table_number, self.__customer_number,  self.__food_number

    def reset_status(self):
        self.__table_number, self.__food_number, \
             self.__customer_number, self.__cooking_time = 0, 0, 0, 0

    def is_cooking(self) -> bool:
        return self.__is_cooking

    def set_is_cooking(self):
        self.__is_cooking = not self.__is_cooking

    def get_left_cooking_time(self) -> int:
        return self.__cooking_time

    def update(self) -> bool:

        if self.__is_cooking:
            self.__cooking_time -= 1
            if self.__cooking_time == 0:
                self.__is_cooking = not self.__is_cooking
                return True
        return False
