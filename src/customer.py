from src.printout import PrintOut
from collections import namedtuple


CustomerInfo = namedtuple('CustomerInfo', 'number, table, food')


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
