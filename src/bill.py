from customer import Customer


class BillManager:

    def __init__(self, waiting_time):

        self.__bill_waiting_queue = []
        self.__billing_time = waiting_time
        self.__elapsed_billing_time = 0
        self.__is_working = False
        self.__current_customer: Customer = None

    def change_working_status(self):
        self.__is_working = not self.__is_working

    def receive_customer(self, customer: Customer):

        print(f"{customer.number}번 손님이 계산대 앞에 줄을 섭니다.")
        self.__bill_waiting_queue.append(customer)

    def process_billing(self, count: int = 1):
        for _ in range(count):
            target = self.__bill_waiting_queue.pop(0)
            self.__current_customer = target
            self.change_working_status()

    def update(self):

        if self.__is_working and self.__current_customer:
            self.__elapsed_billing_time += 1

            if self.__billing_time <= self.__elapsed_billing_time:
                print(f"{self.__current_customer.number}번 손님이 "
                      f"계산을 마치고 레스토랑을 떠났습니다.")

                self.change_working_status()
                self.__current_customer = None

        if self.__bill_waiting_queue and not self.__is_working:
            self.process_billing()
