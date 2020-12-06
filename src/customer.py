from src.printout import PrintOut
from collections import namedtuple


CustomerInfo = namedtuple('CustomerInfo', 'number, table, food', defaults=[0, 0, 0])


class Customer:

    def __init__(self, info: CustomerInfo, eating_time=0, total_time=0):
        self.__info = info
        self.__time = total_time
        self.eating_time = eating_time
        self.eating = False

    @property
    def info(self):
        return self.__info

    @property
    def dish(self):
        return self.eating

    @property
    def time(self):
        return self.__time

    def update(self):
        self.__time -= 1
        if self.eating:
            return self.__time <= 0

        if self.__time <= self.eating_time:
            self.__change_status()
        return False

    def __change_status(self):
        self.eating = not self.eating
        PrintOut.add('start', self.info)
