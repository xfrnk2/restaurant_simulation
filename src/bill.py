from src.printout import PrintOut


class Bill:
    def __init__(self):
        self.waiting = []
        self.__time = 5

    def update(self):
        if not self.waiting:
            return
        self.__time -= 1
        if self.__time < 0:
            self.__time = 5
            PrintOut.add('leave', self.waiting.pop(0))
