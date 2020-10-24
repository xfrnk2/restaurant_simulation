from customer import Customer


class TableManager:

    def __init__(self, table_amount: int):
        self.__table_queue = [0] * table_amount
        self.__finished_eating_queue = []

    @property
    def finished_eating_queue(self):
        return self.__finished_eating_queue

    def get_table_queue(self):
        return self.__table_queue

    def is_exist(self) -> bool:
        return any(self.__table_queue)

    def set_customer(self, customer: Customer):

        for table_number, table in enumerate(self.__table_queue):
            if not table:
                self.__table_queue[table_number] = customer
                return table_number

    def getting_food(self, table_num: int):

        print(f"{self.__table_queue[table_num].number}번 손님이 식사를 시작합니다.")
        self.__table_queue[table_num].change_status_is_eating()

    def is_acceptable(self) -> bool:
        return not all(self.__table_queue)

    def update(self):

        target_customer_queue = []

        for num in range(len(self.__table_queue)):

            if isinstance(self.__table_queue[num], Customer):

                customer = self.__table_queue[num]
                customer.update()

                if customer.check_eating_status:
                    print(f"{num}번 테이블에 앉아있는 {customer.number}번"
                          f" 손님이 식사를 마쳤습니다.")

                    customer.change_status_is_eating()
                    target_customer_queue.append(customer)
                    self.__table_queue[num] = 0

        self.__finished_eating_queue = target_customer_queue
