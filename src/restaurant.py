from src.table import Table
from src.cook import Cook
from src.printer import Printer
from src.customer import CustomerInfo, Customer
from random import randrange


class Restaurant:
    def __init__(self):
        self.__customer_number = 0
        self.__table = Table(20)
        self.__cook = Cook()
        self.waiting = []

        self.food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.time = 0

    def new_customer(self):
        time = randrange(15, 41)
        if not self.__table.is_waitable(waitable_time=time, waiting_amount=len(self.waiting)):
            Printer.add(f'손님이 기다릴 수 없어 돌아갑니다. 현재대기시간 {self.__table.waitable_time}분 / 대기가능시간 {time}분')
            return

        self.__customer_number += 1
        self.waiting.append(self.__customer_number)
        Printer.add(f'{self.__customer_number}번째 손님이 시각 {self.time}분에 레스토랑에 도착했습니다.')

    def update(self):
        self.__table.update()
        self.__cook.update()

        sittable = self.__table.empty()
        while self.waiting and sittable:
            table_num, food_num = sittable.pop(0), randrange(1, 5)
            info = CustomerInfo(self.waiting.pop(0), table_num, food_num)
            cooking_time = self.cooking_time[food_num]

            total_time = self.__cook.waiting_time() + self.eating_time[food_num] + cooking_time
            self.__cook.order_time.append(cooking_time)
            self.__table.table[table_num] = Customer(info, self.eating_time[food_num], total_time)

            Printer.add(f'{info[0]}번 손님이 {info[1]}번 테이블에 앉습니다. {info[0]}번 요리({self.food_name[info[2]]})를 주문합니다.')

    def run(self):
        Printer.init()
        period = 2
        self.time = 1
        while self.time < 721:

            Printer.add(f'[현재시각 : {self.time}분]')
            is_remained = self.time % period

            if not is_remained:
                self.new_customer()
            self.update()
            Printer.output()
            self.time += 1
