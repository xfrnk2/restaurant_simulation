from src.printer import Printer
from src.customer import Customer
from src.bill import Bill


class Table:
    def __init__(self, amount):
        self.table = {i: [] for i in range(1, amount + 1)}
        self.__current_waitable_time = 0
        self.__bill = Bill()

    @property
    def waitable_time(self):
        return self.__current_waitable_time

    def is_waitable(self, waitable_time, waiting_amount):
        entire_table = self.table.values()
        valid_table = tuple(filter(lambda customer: not customer or customer.time <= waitable_time,
                                   entire_table))
        condition = waiting_amount - len(valid_table)

        if condition < 0:
            return True

        entire_table = sorted([customer.time for customer in entire_table])
        if condition < len(self.table):
            self.__current_waitable_time = entire_table[waiting_amount]
        else:
            print(entire_table)
            self.__current_waitable_time = entire_table[-1]
        return False

    def empty(self):
        return list(filter(lambda table_num: not self.table[table_num], self.table.keys()))

    def update(self):
        finished_table = []
        for i in self.table.keys():
            if not isinstance(self.table[i], Customer):
                continue

            if self.table[i].update():
                customer_num = self.table[i].info.number
                self.table[i] = []
                finished_table.append(customer_num)
                Printer.add(f'{customer_num}번 손님이 식사를 마쳤습니다. {customer_num}번 손님이 계산대 앞에 줄을 섭니다.')

        self.__bill.add(finished_table)
        self.__bill.update()
