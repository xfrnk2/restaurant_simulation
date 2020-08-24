from random import randrange
from customer import Customer
from table import TableManager
from kitchen import Kitchen
from bill import BillManager
import sys

class Restaurant:

    def __init__(self, customer_visiting_period : int):
        billing_period = 5
        cash_desk_num = 1
        cooks_num = 3
        table_quantity = 20

        self.__visiting_period = customer_visiting_period
        self.__table_manager = TableManager(table_quantity)
        self.__kitchen = Kitchen(cooks_num)
        self.__bill_manager = BillManager(billing_period, cash_desk_num)

        self.__number_of_customers = 0
        self.__waiting_customers = []

        self.__food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
        self.__food_eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.__food_cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}

    def customer_visiting(self, elapsed_time: int):
        self.__number_of_customers += 1
        new_customer = Customer(self.__number_of_customers, elapsed_time)

        print(f"{self.__number_of_customers}번째 손님이 시각 {elapsed_time} 분에 레스토랑에 도착했습니다.")
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

                if customer.get_elapsed_waiting_time() < customer.get_remaining_time_by_new_table():
                    break

                if customer.get_elapsed_waiting_time() == customer.get_remaining_time_by_new_table() and not self.__table_manager.is_table_full():
                    self.customer_entrance(customer)
                    customer_count += 1

            self.pop_waiting_queue(customer_count)

    def get_time_until_being_allocated_to_cook(self)-> int:
        result = 0
        q = self.__kitchen.get_order_queue()
        if q:
            q = [self.__food_cooking_time[order[0]] for order in q]
            group = self.__kitchen.get_cooks_current_cooking_time()
            q.append(0)

            while q:
                group.sort()
                target = group.pop(0)
                result += target
                group = [i - target for i in group]

                group.append(q.pop(0))
        return result

    def run(self):

        elapsed_time = 0

        while elapsed_time < 720:

            elapsed_time += 1


            table_target_customer_queue = self.__table_manager.update()
            for customer in table_target_customer_queue:
                self.__bill_manager.receive_customer(customer)

            self.__bill_manager.update()

            if self.__table_manager.is_exist():
                finished_order_queue = self.__kitchen.update()

                if finished_order_queue:
                    for order in finished_order_queue:
                        self.__table_manager.getting_food(order)

            self.waiting_update()

            self.__kitchen.start_cooking_update()