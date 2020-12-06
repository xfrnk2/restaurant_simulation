from src.table import Table
from src.bill import Bill
from src.cook import Cook
from src.printout import PrintOut
from src.customer import CustomerInfo, Customer
from random import randrange


class Restaurant:
    def __init__(self):
        self.__customer_number = 0
        self.__table = Table(20)
        self.__waiting = []
        self.__bill = Bill()
        self.__cook = Cook()

        self.cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.time = 0

    def new_customer(self):
        time = randrange(15, 41)
        if not self.__table.is_waitable(waitable_time=time, waiting_amount=len(self.__waiting)):
            PrintOut.add('back', (self.__table.waitable_time, time))
            return

        self.__customer_number += 1
        self.__waiting.append(self.__customer_number)
        PrintOut.add('arrive', (self.__customer_number, self.time))

    def update(self):
        self.__bill.waiting.extend(self.__table.update())
        self.__bill.update()
        self.__cook.update()

        sittable = self.__table.empty()
        while self.__waiting and sittable:
            table_num, food_num = sittable.pop(0), randrange(1, 5)
            info = CustomerInfo(self.__waiting.pop(0), table_num, food_num)
            cooking_time = self.cooking_time[food_num]

            total_time = self.__cook.waiting_time() + self.eating_time[food_num] + cooking_time
            self.__cook.order_time.append(cooking_time)
            self.__table.table[table_num] = Customer(info, self.eating_time[food_num], total_time)

            PrintOut.add('order_request', info)

    def run(self):
        PrintOut.init()
        period = 2
        self.time = 1
        while self.time < 721:

            PrintOut.add('now', self.time)
            if not self.time % period:
                self.new_customer()
            self.update()
            PrintOut.printout()
            self.time += 1
