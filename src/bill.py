from customer import Customer


class BillManager:

    def __init__(self, waiting_time, desk_num):

        self.__waiting_queue = []
        self.__billing_time = waiting_time
        self.__desk_number = desk_num

        self.__finished_queue = []
        self.__desks = {}

    def receive_customer(self, customer: Customer):

        customer_number = customer.number
        print(f"{customer_number}번 손님이 계산대 앞에 줄을 섭니다.")
        self.__waiting_queue.append(customer_number)

    def update(self):

        for customer_number in self.__desks.keys():  # 업데이트
            self.__desks[customer_number] -= 1
            if self.__desks[customer_number] == 0:
                self.__finished_queue.append(customer_number)

        for customer_number in self.__finished_queue:  # 업데이트 연장선으로 끝난 손님 퇴장처리
            self.__desks.pop(customer_number)
            print(f"{customer_number}번 손님이 "
                  f"계산을 마치고 레스토랑을 떠났습니다.")

        self.__finished_queue = []

        while self.__waiting_queue and len(self.__desks) < self.__desk_number:
            k = self.__waiting_queue.pop(0)
            self.__desks[k] = self.__billing_time
