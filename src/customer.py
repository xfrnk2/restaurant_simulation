from random import randrange
from dataclasses import dataclass


class Customer:

    def __init__(self, number: int, arrival_time: int):

        self.__arrival_time = arrival_time
        self.__customer_number = number
        self.__food_num = 0
        self.__info: dataclass = None

        self.__is_eating: bool = False
        self.__elapsed_waiting_time = 0
        self.__waited_time_for_food = 0
        self.__elapsed_eating_time = 0

        self.__remaining_time_by_new_table = 0

        self.__is_bill_waiting: bool = False
        self.__is_billing: bool = False

    def get_total_time(self, until_being_allocated):
        return until_being_allocated + self.__info.cooking_time + self.__info.eating_time

    @property
    def elapsed_waiting_time(self) -> int:
        return self.__elapsed_waiting_time

    @property
    def elapsed_eating_time(self):
        return self.__elapsed_eating_time

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, customer_info):
        self.__info = customer_info

    @property
    def number(self) -> int:
        return self.__customer_number

    @property
    def customer_number(self) -> int:
        return self.__customer_number

    @property
    def is_eating(self) -> bool:
        return self.__is_eating

    @property
    def check_eating_status(self) -> bool:
        return self.__elapsed_eating_time == self.__info.eating_time

    def update(self):
        if self.__is_eating:
            self.__elapsed_eating_time += 1
        else:
            self.__waited_time_for_food += 1

    def waiting_update(self):
        self.__elapsed_waiting_time += 1

    def change_status_is_eating(self):
        self.__is_eating = not self.__is_eating

    @property
    def remaining_time_by_new_table(self):
        return self.__remaining_time_by_new_table

    @remaining_time_by_new_table.setter
    def remaining_time_by_new_table(self, value):
        self.__remaining_time_by_new_table = value

    @property
    def elapsed_waited_time_for_food(self):
        return self.__waited_time_for_food

    def is_billing(self) -> bool:
        return self.__is_billing

    def is_bill_waiting(self) -> bool:
        return self.__is_bill_waiting

    def change_is_bill_waiting_status(self):
        self.__is_bill_waiting = not self.__is_bill_waiting

    def change_is_billing_status(self):
        self.__is_billing = not self.__is_billing
