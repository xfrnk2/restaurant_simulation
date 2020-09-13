from dataclasses import dataclass
from restaurant_object import RestaurantObject
from customer import Customer
from cook import Cook


@dataclass()
class CookingRequest:
    table_num: int
    customer_num: int
    food_num: int
    cooking_time: int


class Kitchen(RestaurantObject):

    def __init__(self, cook_num: int):

        self.__cook_number = cook_num
        self.__cooks = [Cook() for _ in range(cook_num)]
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

            for cook in self.__cooks:
                if not self.__order_queue:
                    break
                if not cook.is_cooking:
                        customer_food_num, customer_num, table_number = self.__order_queue.pop(0)
                        cook.set_request(CookingRequest(table_num=table_number, customer_num=customer_num, food_num=customer_food_num, cooking_time=self.__food_cooking_time[customer_food_num]))

    def update(self) -> list:

        finished_order_queue = []

        for cook in self.__cooks:
            if cook.update():
                info = cook.get_order_info()
                table_num, customer_num, food_num = info

                print(f"{customer_num}번 손님의 {food_num}번"
                      f"요리({self.__food_name[food_num]}) 조리가 끝났습니다.")

                cook.reset_status()

                finished_order_queue.append(info)

        return finished_order_queue
