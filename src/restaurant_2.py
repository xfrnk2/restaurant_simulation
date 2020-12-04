from collections import namedtuple

CustomerInfo = namedtuple('CustomerInfo', 'number, table, food')




class Customer:

    def __init__(self, number, table, food, time):
        self.__info = CustomerInfo(number = number, table = table, food = food)
        self.__time = time
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

    def __update(self):
        self.__time -= 1
        return self.__time < 0

    def __change_status(self, time):
        self.__time = time
        self.__eating = not self.__eating


class Table:

    def __init__(self, amount):
        self.table = {i: j for i, j in zip(range(1, amount + 1), [None] * amount)}
        self.__cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.__cook = []

    def __update(self):
        finish = []

        for i in self.table.keys():
            if not isinstance(self.table[i], Customer):
                continue

            if self.table[i].__update():
                if not self.table[i].dish:
                    time = self.__eating_time[self.table[i].info.food]
                    self.table[i].__change_status(time)
                    continue

                finish.append(self.table[i].info.number)

        return finish

    def empty(self):
        empty = []
        for key in self.table.keys():
            if not self.table[key]:
                empty.append(key)
        return empty


class LogicTable:
    def __init__(self, amount):
        self.__table = Table(amount)
        self.__current_waitable_time = 0
        self.__cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__eating_time = {1: 30, 2: 20, 3: 15, 4: 10}

    @property
    def table(self):
        return self.__table

    @property
    def waitable_time(self):
        return self.__current_waitable_time

    def is_waitable(self, waitable_time, waiting_amount):

        available = [customer.time for customer in self.__table.table.values() if customer.time <= waitable_time]
        if waiting_amount - len(available) < 0:
            return True

        if waiting_amount - len(available) < len(self.__table.table):
            self.__current_waitable_time = available[waiting_amount].time
        else:
            self.__current_waitable_time = available[-1].time
        return False









class Bill:
    def __init__(self):
        self.__waiting = []
        self.__time = 5

    def new(self, customer: int):
        self.__waiting.append(customer)

    def __update(self):
        self.__time -= 1
        if self.__time < 0:
            self.__time = 5
            self.__waiting.pop(0)
            #문구
