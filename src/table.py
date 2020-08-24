from restaurant_object import RestaurantObject


class TableManager(RestaurantObject):

    def __init__(self, table_amount: int):
        self.__table_queue = [0] * (table_amount)

    def update(self):
        pass