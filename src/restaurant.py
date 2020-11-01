from random import randrange
from customer import Customer
from table import TableManager
from kitchen import Kitchen
from bill import BillManager


class Restaurant:

    def __init__(self, customer_visiting_period: int):

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

                can_entrance = customer.get_remaining_time_by_new_table() <= customer.get_elapsed_waiting_time()

                if not can_entrance:
                    break

                if can_entrance and not self.__table_manager.is_table_full():
                    self.customer_entrance(customer)
                    customer_count += 1

            self.pop_waiting_queue(customer_count)

    def get_time_until_being_allocated_to_cook(self) -> int:

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

    def customer_entrance(self, customer: Customer):

        food_num = randrange(1, 5)
        food_eating_time = self.__food_eating_time[food_num]
        food_cooking_time = self.__food_cooking_time[food_num]
        customer.set_attribute((food_num, food_eating_time, food_cooking_time))

        table_num = self.__table_manager.set_customer(customer)
        customer_number = customer.get_customer_number()
        until_being_allocated = self.get_time_until_being_allocated_to_cook()

        total_time = until_being_allocated + customer.get_food_cooking_time() + customer.get_food_eating_time()
        customer.set_total_time(total_time)

        print(f"{customer_number}번 손님이 {table_num}번 테이블에 앉습니다.")
        print(f"{customer_number}번 손님이 {food_num}번 요리"
              f" ({self.__food_name[food_num]})를 주문합니다.")

        self.__kitchen.get_order_from_new_customer(customer, table_num)

    def is_possible_to_wait(self, new_customer: Customer) -> bool:

        n = 0
        lower_time_group = []
        higher_time_group = []

        for table in self.__table_manager.get_table_queue():
            remaining_time = table.get_total_time() - \
                            (table.get_elapsed_waited_time_for_food() +
                             table.get_elapsed_eating_time())

            if remaining_time < new_customer.get_maximum_waiting_time():
                n += 1
                lower_time_group.append(remaining_time)
            else:
                higher_time_group.append(remaining_time)

        if self.__waiting_customers:
            if len(self.__waiting_customers) < n:
                new_customer.set_remaining_time_by_new_table(sorted(lower_time_group)[len(self.__waiting_customers)])
                return True

        else:
            if 1 <= n:
                new_customer.set_remaining_time_by_new_table(
                    min(lower_time_group))
                return True

        applicable_index = sorted(
            higher_time_group)[len(self.__waiting_customers) - n]
        new_customer.set_remaining_time_by_new_table(applicable_index)
        return False

    def run(self):

        elapsed_time = 0

        while elapsed_time < 720:

            elapsed_time += 1
            table_target_customer_queue = self.__table_manager.update()

            for customer in table_target_customer_queue:
                self.__bill_manager.receive_customer(customer)

            self.__bill_manager.update()

            self.__kitchen.update()

            for table_num in self.__kitchen.finished_table_numbers:
                self.__table_manager.getting_food(table_num)

            self.waiting_update()

            if elapsed_time % self.__visiting_period == 0:
                customer = self.customer_visiting(elapsed_time)

                if self.__table_manager.is_table_full():
                    if self.is_possible_to_wait(customer):
                        self.receive_customer(customer)
                    else:
                        print(f"손님이 기다릴 수 없어 돌아갑니다.\n현재 대기 시간"
                              f"{customer.get_elapsed_waiting_time()}분"
                              f" / 대기 가능 시간 "
                              f"{customer.get_remaining_time_by_new_table()}분")

                else:
                    self.customer_entrance(customer)

            self.__kitchen.start_cooking_update()
