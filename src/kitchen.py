from restaurant_object import RestaurantObject
from cook import Cook

class Kitchen(RestaurantObject):

    def __init__(self, cook_num: int):

        self.__cook_number = cook_num
        self.__cooks = [Cook() for _ in range(cook_num)]
        self.__food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.__order_queue = []

    def update(self):
        pass