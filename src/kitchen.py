from dataclasses import dataclass
from cook import Cook


class Kitchen:

    def __init__(self, cook_num: int):

        self.__cook_number = cook_num
        self.__cooks = []
        self.__food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__food_eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.__food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.__order_queue = []
        self.__finished_table_numbers = []

    @property
    def cooks(self):
        return self.__cooks

    @property
    def order_queue(self):
        return self.__order_queue

    @property
    def finished_table_numbers(self):
        return self.__finished_table_numbers

    def get_new_customer_info(
         self, customer_info: dataclass):
        self.__order_queue.append(customer_info)

    def start_cooking_update(self):
        while self.__order_queue and len(self.__cooks) < self.__cook_number:
            self.__cooks.append(Cook(self.__order_queue.pop(0)))

    def update(self):

        finished_table_numbers = []
        finished_order = []
        cooks = [cook if not cook.update() else finished_order.append(cook.order_info) for cook in self.__cooks]
        self.__cooks = list(filter(None, cooks))

        if finished_order:
            for info in finished_order:
                print(f"{info.customer_num}번 손님의 {info.food_num}번"
                      f"요리({self.__food_name[info.food_num]}) 조리가 끝났습니다.")
                finished_table_numbers.append(info.table_num)

        self.__finished_table_numbers = finished_table_numbers
