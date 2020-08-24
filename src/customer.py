from restaurant_object import RestaurantObject
from random import randrange

class Customer(RestaurantObject):

    def __init__(self, number ,arrival_time):

        self.__arrival_time = arrival_time
        self.__maximum_waiting_time = randrange(15, 41)

        self.__customer_number = number
        self.__food_num = 0
        self.__food_eating_time = 0
        self.__food_cooking_time = 0

        self.__is_eating: bool = False
        self.__elapsed_waiting_time = 0
        self.__waited_time_for_food = 0
        self.__elapsed_eating_time = 0

        self.__total_time = 0
        self.__remaining_time_by_new_table = 0
