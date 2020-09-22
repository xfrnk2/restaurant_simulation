from customer import Customer


class CashDesk:

    def __init__(self, billing_time: int):
        self.__customer_number = None
        self.__billing_time = billing_time
        self.__elapsed_billing_time = 0
        self.__is_working = False

    def receive_customer(self, customer: Customer):
        self.__customer_number = customer.get_request()[0]

    def update(self):

        if self.__is_working:
            self.__elapsed_billing_time += 1

            if self.__billing_time <= self.__elapsed_billing_time:
                self.change_cash_desk_status()
                return True

        return False

    def is_working(self):
        return self.__is_working

    def change_cash_desk_status(self):
        self.__elapsed_billing_time = 0
        self.__is_working = not self.__is_working

    def get_customer_info(self):
        return self.__customer_number


class BillManager:

    def __init__(self, waiting_time, cash_desk_num):

        self.__bill_waiting_queue = []
        self.__cash_desk_num = cash_desk_num
        self.__cash_desk = CashDesk(waiting_time)

    def receive_customer(self, customer: Customer):
        invalid = customer.is_billing() or customer.is_bill_waiting()
        #TODO-아예 valid한 상태만 있다면 전체적인 구조 개선이 필요합니다.
        assert not invalid, "초기 상태에서는 invalid 할 수 없습니다."

        print(f"{customer.get_customer_number()}번 손님이 계산대 앞에 줄을 섭니다.")
        customer.change_is_bill_waiting_status()
        self.__bill_waiting_queue.append(customer)

    def update(self):

        if self.__cash_desk.update():
            print(f"{self.__cash_desk.get_customer_info()}번 손님이 "
                  f"계산을 마치고 레스토랑을 떠났습니다.")

        if self.__bill_waiting_queue and \
           not self.__cash_desk.is_working():
            target = self.__bill_waiting_queue.pop(0)
            target.change_is_billing_status()
            target.change_is_bill_waiting_status()
            self.__cash_desk.receive_customer(target)
            self.__cash_desk.change_cash_desk_status()
