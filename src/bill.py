from src.printout import Printout
BILLING_CYCLE = 5


class Bill:
    def __init__(self):
        self.waiting = []
        self.time = BILLING_CYCLE

    def update(self):
        if not self.waiting:
            return
        self.time -= 1
        if self.time < 0:
            self.time = 5
            Printout.add(f'{self.waiting.pop(0)}번 손님이 계산을 마치고 레스토랑을 떠났습니다.')

    def add(self, numbers):
        self.waiting.extend(numbers)
        return
