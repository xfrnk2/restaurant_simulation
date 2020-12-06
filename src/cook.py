

class Cook:
    def __init__(self):

        self.order = []
        self.cooks = []

    def waiting_time(self):
        result = 0
        if self.order:
            order, cooks = self.order, self.cooks
            order.append(0)
            while order and cooks:
                cooks.sort()
                target = cooks.pop(0)
                result += target
                cooks = list(map(lambda x: x - target, cooks))
                cooks.append(order.pop(0))
        return result

    def available_new_order(self) -> int:
        order_num, cook_num = len(self.order), 3 - len(self.cooks)
        if order_num < cook_num:
            return order_num
        return cook_num

    def update(self):
        cooks = list(map(lambda x: x - 1, self.cooks))
        self.cooks = list(filter(lambda x: 0 < x, cooks))
        pivot = self.available_new_order()
        self.cooks += self.order[:pivot]
        self.order = self.order[pivot:]
