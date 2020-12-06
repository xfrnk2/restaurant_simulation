from src.printout import PrintOut
from src.customer import Customer
import sys


class Default:
    def __init__(self):
        self.__time = sys.maxsize

    @property
    def time(self):
        return self.__time


class Table:
    def __init__(self, amount):
        self.table = {i: j for i, j in zip(range(1, amount + 1), [Default()] * amount)}
        self.__current_waitable_time = 0

    @property
    def waitable_time(self):
        return self.__current_waitable_time

    def is_waitable(self, waitable_time, waiting_amount):
        entire_table = self.table.values()
        valid_table = tuple(filter(lambda customer: isinstance(customer, Default) or customer.time <= waitable_time,
                                   entire_table))
        condition = waiting_amount - len(valid_table)

        if condition < 0:
            return True

        entire_table = sorted([customer.time for customer in entire_table])
        if condition < len(self.table):
            self.__current_waitable_time = entire_table[waiting_amount]
        else:
            self.__current_waitable_time = entire_table[-1]
        return False

    def empty(self):
        return list(filter(lambda key: isinstance(self.table[key], Default), self.table.keys()))

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
