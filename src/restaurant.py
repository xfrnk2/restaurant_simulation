from collections import namedtuple
from random import randrange
import sys
CustomerInfo = namedtuple('CustomerInfo', 'number, table, food')


class Default:
    def __init__(self):
        self.__time = sys.maxsize

    def __update(self):
        return False

    @property
    def time(self):
        return self.__time


class PrintOut:
    @staticmethod
    def init():
        __class__.__queue = []
        __class__.__messages = {
            'arrive': 'f"{info[0]}번째 손님이 시각 {info[1]}분에 레스토랑에 도착했습니다."',
            'back': 'f"손님이 기다릴 수 없어 돌아갑니다. 현재 대기 시간 {info[0]} / 대기 가능 시간 {info[1]}"',
            'order_request': 'f"{info[0]}번 손님이 {info[1]}번 테이블에 앉습니다. {info[0]}번 손님이 {info[2]}번 요리({__class__.food_name[info[2]]})를 주문합니다."',
            'start': 'f"{info[0]}번 손님의 {info[2]}번 요리({__class__.food_name[info[2]]}) 조리가 끝났습니다. {info[0]}번 손님이 식사를 시작합니다."',
            'finish': 'f"{info}번 손님이 식사를 마쳤습니다. {info}번 손님이 계산대 앞에 줄을 섭니다."',
            'leave': 'f"{info}번 손님이 계산을 마치고 레스토랑을 떠났습니다."',
            'now': 'f"현재시각{info}분"'
            }

    @staticmethod
    def add(sign: str, info: tuple or int):
        __class__.__queue.append((sign, info))

    @staticmethod
    def printout():
        if not __class__.__queue:
            return

        for sign, info in __class__.__queue:
            print(eval(__class__.__messages[sign]))
        __class__.__queue = []

    __queue = []
    __messages = {}
    food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}


class Customer:

    def __init__(self, info: CustomerInfo, eating_time, total_time):
        self.__info = info
        self.__time = total_time
        self.__eating_time = eating_time
        self.__eating = False

    @property
    def info(self):
        return self.__info

    @property
    def dish(self):
        return self.__eating

    @property
    def time(self):
        return self.__time

    def update(self):
        self.__time -= 1
        if self.__eating:
            return self.__time <= 0

        if self.__time <= self.__eating_time:
            self.__change_status()
        return False

    def __change_status(self):
        self.__eating = not self.__eating
        PrintOut.add('start', self.info)


class Cook:
    def __init__(self):

        self.order = []
        self.cooks = []

    def waiting_time(self):
        result = 0
        if self.order:
            order, cooks = self.order, self.cooks
            order.append(0)
            while order and cooks:
                cooks.sort()
                target = cooks.pop(0)
                result += target
                cooks = list(map(lambda x: x - target, cooks))#[i - target for i in cooks]
                cooks.append(order.pop(0))
        return result

    def available_new_order(self):
        order_num, cook_num = len(self.order), 3 - len(self.cooks)
        if order_num < cook_num:
            return order_num
        return cook_num

    def update(self):
        cooks = list(map(lambda x: x - 1, self.cooks))
        self.cooks = list(filter(lambda x: 0 < x, cooks))
        pivot = self.available_new_order()
        self.cooks += self.order[:pivot] #error 발생 주의?
        self.order = self.order[pivot:]

    def new_order(self, order):
        cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.order.append(cooking_time[order])

class Table:

    def __init__(self, amount):
        self.table = {i: j for i, j in zip(range(1, amount + 1), [Default()] * amount)}

    def update(self):
        finish = []

        for i in self.table.keys():
            if not isinstance(self.table[i], Customer):
                continue

            if self.table[i].update():
                customer_num = self.table[i].info.number
                self.table[i] = Default()
                finish.append(customer_num)
                PrintOut.add('finish', customer_num)



        return finish

    def empty(self):
        empty = []
        for key in self.table.keys():
            if isinstance(self.table[key], Default):
                empty.append(key)
        return empty


class LogicTable:
    def __init__(self, amount):
        self.__table = Table(amount)
        self.__current_waitable_time = 0

    @property
    def table(self):
        return self.__table

    @property
    def waitable_time(self):
        return self.__current_waitable_time

    def is_waitable(self, waitable_time, waiting_amount):
        available = [customer.time for customer in self.__table.table.values() if isinstance(customer, Default) or customer.time <= waitable_time]

        if waiting_amount - len(available) < 0:
            return True

        entire_table = sorted([customer.time for customer in self.__table.table.values()])
        if waiting_amount - len(available) < len(self.__table.table):
            if waiting_amount:
                self.__current_waitable_time = entire_table[waiting_amount]
        else:
            self.__current_waitable_time = entire_table[-1]
        return False


class Bill:
    def __init__(self):
        self.waiting = []
        self.__time = 5

    def new(self, customer: int):
        self.waiting.append(customer)

    def update(self):
        if not self.waiting:
            return
        self.__time -= 1
        if self.__time < 0:
            self.__time = 5
            PrintOut.add('leave', self.waiting.pop(0))
            #문구


class Management:
    def __init__(self):
        self.__customer_number = 0
        self.table = LogicTable(20)
        self.waiting = []
        self.bill = Bill()
        self.cook = Cook()
        self.cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.time = 0

    def new_customer(self):
        time = randrange(15, 41)
        if self.table.is_waitable(waitable_time=time, waiting_amount=len(self.waiting)):
            self.__customer_number += 1
            self.waiting.append(self.__customer_number)
            #새 손님 도착
            PrintOut.add('arrive', (self.__customer_number, self.time))
            return
        PrintOut.add('back', (self.table.waitable_time, time))
        #손님 퇴장, 기다릴 시간 구하여 출력


    def update(self): # waiting update
        #table 업데이트
        self.bill.waiting.extend(self.table.table.update())
        self.bill.update()
        self.cook.update()


        sittable = self.table.table.empty()
        while self.waiting and sittable:
            table_num, food_num = sittable.pop(0), randrange(1, 5)
            info = CustomerInfo(self.waiting.pop(0), table_num, food_num)
            total_time = self.cook.waiting_time() + self.eating_time[food_num] + self.cooking_time[food_num]
            self.table.table.table[table_num] = Customer(info, self.eating_time[food_num], total_time)
            self.cook.new_order(food_num)
            PrintOut.add('order_request', info)

    def run(self):
        PrintOut.init()
        period = 2
        self.time = 1
        while self.time < 720:

            PrintOut.add('now', self.time)
            if not self.time % period:
                self.new_customer()
            self.update()
            PrintOut.printout()
            self.time += 1


a = Management()
a.run()