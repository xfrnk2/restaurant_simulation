from restaurant_object import RestaurantObject


class Cook(RestaurantObject):
    def __init__(self):
        self.__food_number = 0
        self.__cooking_time = 0
        self.__customer_number = 0
        self.__table_number = 0
        self.__is_cooking = False