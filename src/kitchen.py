from dataclasses import dataclass
from customer import Customer
from cook import Cook


@dataclass()
class CookingRequest:
    table_num: int
    customer_num: int
    food_num: int
    cooking_time: int


class Kitchen:

    def __init__(self, cook_num: int):

        self.__cook_number = cook_num
        self.__cooks = []
        self.__food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.__order_queue = []

    def get_order_queue(self):
        return self.__order_queue

    def get_cooks_current_cooking_time(self) -> list:
        return [cook.get_left_cooking_time() for cook in self.__cooks]

    def get_order_from_new_customer(
         self, customer: Customer, table_number: int):

        customer_num, customer_food_num = customer.get_request()
        info = customer_food_num, customer_num, table_number
        self.__order_queue.append(info)

    def start_cooking_update(self):
            while self.__order_queue and len(self.__cooks) < self.__cook_number:
                customer_food_num, customer_num, table_number = self.__order_queue.pop(0)
                self.__cooks.append(Cook(CookingRequest(table_num=table_number, customer_num=customer_num, food_num=customer_food_num,
                                   cooking_time=self.__food_cooking_time[customer_food_num])))

    def update(self) -> list:
        finished_order_queue = []

        if self.__cooks:
            cooks = []
            updating = [cook if cook.update() else cooks.append(cook) for cook in self.__cooks]
            targets = list(filter(None, updating))

            if targets:
                for cook in targets:
                    info = cook.get_order_info()
                    print(f"{info.customer_num}번 손님의 {info.food_num}번"
                          f"요리({self.__food_name[info.food_num]}) 조리가 끝났습니다.")
                    finished_order_queue.append(info)

                self.__cooks = cooks
        return finished_order_queue
