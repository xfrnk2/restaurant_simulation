from random import randrange

class Initialize:

    @staticmethod
    def init():
        pass

    @staticmethod
    def order(customer, food, table):
        return [__class__.cooking_time[food], customer, food, table]

    @staticmethod
    def table(customer, food):
        return [__class__.eating_time[food], __class__.eating_time[food], customer]

    cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
    eating_time = {1: 30, 2: 20, 3: 15, 4: 10}


class PrintOut:
    @staticmethod
    def init():
        __class__.__queue = []
        __class__.__messages = {'arrive': 'f"{info[0]}번째 손님이 시각 {info[1]}분에 레스토랑에 도착했습니다."',
                'back': 'f"손님이 기다릴 수 없어 돌아갑니다. 현재 대기 시간 {info[0]} / 대기 가능 시간 {info[1]}"',
                'order_request': 'f"{info[0]}번 손님이 {info[1]}번 테이블에 앉습니다. {info[0]}번 손님이 {info[2]}번 요리({__class__.food_name[info[2]]})를 주문합니다."',
                'start': 'f"{info[0]}번 손님의 {info[1]}번 요리({__class__.food_name[info[1]]}) 조리가 끝났습니다. {info[0]}번 손님이 식사를 시작합니다."',
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
class Operation:
    pass


class Bill:
    def __init__(self):
        self.__waiting = []
        self.__count = 5

    def append(self, customer):
        self.__waiting.append(customer)

    def update(self):
        if not self.__waiting:
            return

        self.__count -= 1
        if self.__count <= 0:
            PrintOut.add('leave', self.__waiting.pop(0))
            self.__count = 5

PERIOD = 5




class Restaurant:

    def __init__(self):
        PrintOut.init()
        self.__elapsed_time = 0
        self.__customer_number = 0
        self.__table = {i: [0, 0, 0] for i in range(1, 21)}
        self.__order = []
        self.__cook = []
        self.__waiting = []
        self.__bill = Bill()


    def run(self):
        while self.__elapsed_time < 720:
            self.__elapsed_time += 1
            if not self.__elapsed_time % PERIOD:
                self.__visiting()
            self.__update()
            PrintOut.printout()

    def __update(self):
        self.__table_update()
        self.__bill.update()
        self.__cook_update()
        self.__waiting_update()

    def __table_update(self):

        finished = []
        if self.__elapsed_time < 10:
            return
        for i, table in self.__table.items():
            if table[0] != table[1]:
                self.__table[i][0] -= 1
                if table[0] < 0:
                    finished.append(table[2])
                    self.__table[i] = [0, 0, 0]

        if finished:
            for customer in finished:
                self.__bill.append(customer)
                PrintOut.add('finish', customer)

    def __cook_update(self):

        cooks = sorted(self.__cook, key=lambda x: x[0])
        idx = 0
        for i, cook in enumerate(cooks):
            cooks[i][0] -= 1
            if cook[0] < 1:
                idx += 1

        self.__cook = cooks[idx:]
        for order in cooks[:idx]:
            self.__table[order[3]][0] -= 1
            PrintOut.add('start', order[1:])

    def __visiting(self):
        self.__customer_number += 1
        PrintOut.add('arrive', (self.__customer_number, self.__elapsed_time))

        waitable_time = randrange(15, 41)
        waiting_amount = len(self.__waiting)
        for table in self.__table.values():
            if table[0] <= waitable_time:
                waiting_amount -= 1
            if waiting_amount < 0:
                self.__waiting.append(self.__customer_number)
                return

        available = sorted(self.__table.values(), key=lambda x: x[0])
        if waiting_amount < len(self.__table):
            available = available[len(self.__waiting)][0]
        else:
            available = available[-1][0]

        PrintOut.add('back', (f'{available}분', f'{waitable_time}분'))

    def available_new_order(self, cooks_num, new_orders):
        result = 0
        while cooks_num < 3 and 0 < new_orders:
            result += 1
            cooks_num += 1
            new_orders -= 1
        return result

    def __waiting_update(self):
        if self.__waiting:
            sittable_table = [key for key, value in self.__table.items() if value == [0, 0, 0]]

            while self.__waiting and sittable_table:
                customer = self.__waiting.pop(0)
                food = randrange(1, 5)
                table_num = sittable_table.pop(0)
                self.__table[table_num] = Initialize.table(customer, food)
                self.__order.append(Initialize.order(customer, food, table_num))
                PrintOut.add('order_request', (customer, table_num, food))

        for _ in range(self.available_new_order(len(self.__cook), len(self.__order))):
            self.__cook.append(self.__order.pop(0))


restaurant_ = Restaurant()
restaurant_.run()