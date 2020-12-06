

class Cook:
    def __init__(self):

        self.order_time = []
        self.cooks_time = []

    def waiting_time(self):
        result = 0
        if self.order_time:
            order_time, cooks_time = self.order_time, self.cooks_time
            order_time.append(0)
            while order_time and cooks_time:
                cooks_time.sort()
                target_time = cooks_time.pop(0)
                result += target_time
                cooks_time = list(map(lambda cook_time: cook_time - target_time, cooks_time))
                cooks_time.append(order_time.pop(0))
        return result

    def available_new_order(self) -> int:
        order_num, cook_num = len(self.order_time), 3 - len(self.cooks_time)
        if order_num < cook_num:
            return order_num
        return cook_num

    def update(self):
        cooks = list(map(lambda cook_time: cook_time - 1, self.cooks_time))
        self.cooks_time = list(filter(lambda cook_time: 0 < cook_time, cooks))
        pivot = self.available_new_order()
        self.cooks_time += self.order_time[:pivot]
        self.order_time = self.order_time[pivot:]
