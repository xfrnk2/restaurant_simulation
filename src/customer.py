from src.printer import Printer
from collections import namedtuple

CustomerInfo = namedtuple('CustomerInfo', 'number, table, food', defaults=[0, 0, 0])
FOOD_NAME = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}


class Customer:

    def __init__(self, info: CustomerInfo, eating_time=0, total_time=0):
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
        print(self.info)
        Printer.add(f'{self.info.number}번 손님의 {self.info.food}번 요리({FOOD_NAME[self.info.food]}) 조리가 끝났습니다.'
                    f'{self.info.number}번 손님이 식사를 시작합니다.')
