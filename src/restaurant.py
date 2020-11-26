from random import randrange
from src.customer import Customer
from src.table import TableManager
from src.kitchen import Kitchen
from src.bill import BillManager
from typing import NamedTuple


class CustomerInfo(NamedTuple):
    table_num: int = 0
    customer_num: int = 0
    food_num: int = 0
    cooking_time: int = 0
    eating_time: int = 0


class Restaurant:

    def __init__(self, customer_visiting_period: int):

        billing_period = 5
        cooks_num = 3
        table_quantity = 20
        desk_num = 1

        self.__visiting_period = customer_visiting_period
        self.__table_manager = TableManager(table_quantity)
        self.__kitchen = Kitchen(cooks_num)
        self.__bill_manager = BillManager(billing_period, desk_num)

        self.__number_of_customers = 0
        self.__waiting_customers = []

        self.__food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.__food_eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.__food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}

    def customer_visiting(self, elapsed_time: int):

        self.__number_of_customers += 1
        new_customer = Customer(self.__number_of_customers, elapsed_time)

        print(f"{self.__number_of_customers}번째 손님이 시각 "
              f"{elapsed_time} 분에 레스토랑에 도착했습니다.")
        return new_customer

    def receive_customer(self, customer: Customer):
        self.__waiting_customers.append(customer)

    def pop_waiting_queue(self, pop_count: int):

        if pop_count != 0:
            for _ in range(pop_count):
                self.__waiting_customers.pop(0)

    def waiting_update(self):

        if self.__waiting_customers:
            customer_count = 0

            for customer in self.__waiting_customers:
                customer.waiting_update()

            for customer in self.__waiting_customers:
                acceptable = customer.is_waitable and self.__table_manager.is_acceptable()

                if not acceptable:
                    break
                self.customer_entrance(customer)
                customer_count += 1

            self.pop_waiting_queue(customer_count)

    def get_time_until_being_allocated_to_cook(self) -> int:

        result = 0
        queue = self.__kitchen.order_queue
        if queue:
            queue = [self.__food_cooking_time[customer.food_num] for customer in queue]
            remaining_cooking_times = [cook.get_left_cooking_time() for cook in self.__kitchen.cooks]
            queue.append(0)

            while queue and remaining_cooking_times:
                remaining_cooking_times.sort()
                target = remaining_cooking_times.pop(0)
                result += target
                remaining_cooking_times = [i - target for i in remaining_cooking_times]

                remaining_cooking_times.append(queue.pop(0))
        return result

    def customer_entrance(self, customer: Customer):

        food_num = randrange(1, 5)
        table_num = self.__table_manager.set_customer(customer)
        customer_number = customer.number
        customer.info = CustomerInfo(table_num=table_num, customer_num=customer_number, food_num=food_num,
                                     cooking_time=self.__food_cooking_time[food_num], eating_time=self.__food_eating_time[food_num])

        print(f"{customer_number}번 손님이 {table_num}번 테이블에 앉습니다.")
        print(f"{customer_number}번 손님이 {food_num}번 요리"
              f" ({self.__food_name[food_num]})를 주문합니다.")

        self.__kitchen.get_new_customer_info(customer.info)

    def is_possible_to_wait(self, new_customer: Customer) -> bool:

        n = 0
        lower_time_group = []
        higher_time_group = []
        time_until_being_allocated_to_cook = self.get_time_until_being_allocated_to_cook()

        for customer in self.__table_manager.get_table_queue():
            remaining_time = customer.get_total_time(time_until_being_allocated_to_cook)

            if remaining_time < randrange(15, 41):
                n += 1
                lower_time_group.append(remaining_time)
            else:
                higher_time_group.append(remaining_time)

        if self.__waiting_customers:
            if len(self.__waiting_customers) < n:
                new_customer.remaining_time_by_new_table = sorted(lower_time_group)[len(self.__waiting_customers)]
                return True

        else:
            if 1 <= n:
                new_customer.remaining_time_by_new_table = min(lower_time_group)
                return True

        applicable_index = sorted(
            higher_time_group)[len(self.__waiting_customers) - n]
        new_customer.remaining_time_by_new_table = applicable_index
        return False

    def run(self):

        elapsed_time = 0
        simulation_execution = elapsed_time < 720

        while simulation_execution:

            elapsed_time += 1
            self.__table_manager.update()

            for customer in self.__table_manager.finished_eating_queue:
                self.__bill_manager.receive_customer(customer)

            self.__bill_manager.update()

            self.__kitchen.update()

            for table_num in self.__kitchen.finished_table_numbers:
                self.__table_manager.getting_food(table_num)

            self.waiting_update()

            if elapsed_time % self.__visiting_period == 0:
                customer = self.customer_visiting(elapsed_time)

                if self.__table_manager.is_acceptable():
                    self.customer_entrance(customer)

                else:
                    if self.is_possible_to_wait(customer):
                        self.receive_customer(customer)
                    else:
                        print(f"손님이 기다릴 수 없어 돌아갑니다.\n현재 대기 시간"
                              f"0분"
                              f" / 대기 가능 시간 "
                              f"{customer.remaining_time_by_new_table}분")

            self.__kitchen.start_cooking_update()
            elapsed_time += 1
            simulation_execution = elapsed_time < 720


def waiting_checker(tables, waiting_amount, waitable_time):

    for time in tables:
        if time <= waitable_time:
            waiting_amount -= 1
    return waiting_amount < 0


def estimated_waiting_time(tables, waiting_amount):
    if waiting_amount < len(tables):
        return f"{sorted(tables)[waiting_amount]}분"
    return f"{max(tables)}분 이상"


def available_table(tables):

    for idx, table in enumerate(tables):
        if not table:
            return idx+1
    return 0


def table_initialize(customer_num, num):
    food_eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
    return [False, food_eating_time[num]], customer_num


def order_initialize(customer_num, num, table_idx):
    food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
    return [food_cooking_time[num], (customer_num, num, table_idx)]


def cooks_update(cooks):
    cooks = sorted(cooks, key=lambda x: x[0])
    idx = 0
    for i, cook in enumerate(cooks):
        cooks[i][0] -= 1
        if cook[0] < 1:
            idx += 1
    return cooks[idx:], cooks[:idx]


def available_new_order(max_cooks_num, cooks_num, new_orders):
    result = 0
    while cooks_num < max_cooks_num and 0 < new_orders:
        result += 1
        cooks_num += 1
        new_orders -= 1

    return result


def tables_update(tables):
    finished_tables = []

    _tables = tables[:]
    idx = 0

    for table in _tables:
        if not table["is_eating"]:
            idx += 1
            continue
        if 0 < table["eating_time"]:
            table["eating_time"] -= 1
        if table["eating_time"] <= 0:
            finished_tables.append(tables.pop(idx)["customer_num"])

    return tables, finished_tables


class PrintOut:

    @staticmethod
    def init():
        __class__.__queue = []

    @staticmethod
    def add(sign: str, info: tuple):
        __class__.__queue.append((sign, info))

    @staticmethod
    def printout():
        messages = {'arrive': 'f"{info[0]}번째 손님이 시각 {info[1]}분에 레스토랑에 도착했습니다."',
                    'back': 'f"손님이 기다릴 수 없어 돌아갑니다. 현재 대기 시간 {info[0]}분 / 대기 가능 시간 {info[1]}분"',
                    'order_request': 'f"{info[0]}번 손님이 {info[1]}번 테이블에 앉습니다. {info[0]}번 손님이 {info[2]}번 요리({info[3]})를 주문합니다."',
                    'start': 'f"{info[0]}번 손님의 {info[1]}번 요리({info[2]}) 조리가 끝났습니다. {info[0]}번 손님이 식사를 시작합니다."',
                    'finish': 'f"{info}번 손님이 식사를 마쳤습니다. {info}번 손님이 계산대 앞에 줄을 섭니다."',
                    'leave': 'f"{info}번 손님이 계산을 마치고 레스토랑을 떠났습니다."'
                    }
        for sign, info in __class__.__queue:
            print(eval(messages[sign]))

    __queue = []
