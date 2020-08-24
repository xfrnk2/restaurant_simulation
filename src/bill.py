from restaurant_object import RestaurantObject


class CashDesk(RestaurantObject):

    def __init__(self, billing_time: int):
        self.__customer_number = None
        self.__billing_time = billing_time
        self.__elapsed_billing_time = 0
        self.__is_working = False

    def update(self):
        pass


class BillManager(RestaurantObject):

    def __init__(self, waiting_time, cash_desk_num):

        self.__bill_waiting_queue = []
        self.__cash_desk_num = cash_desk_num
        self.__cash_desk_object = CashDesk(waiting_time)

    def update(self):
        pass

