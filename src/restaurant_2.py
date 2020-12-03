

class Customer:

    def __init__(self, number, table, food):
        self.__info = (number, table, food)
        self.__time = 0
        self.__eating = False

    @property
    def info(self):
        return self.__info

    @property
    def complete(self):
        return self.__eating

    def __update(self):
        self.__time -= 1
        return self.__time < 0

    def __change_status(self, time):
        self.__time = time
        self.__eating = not self.__eating

class Table:

    def __init__(self, amount):
        self.table = {i: j for i, j in zip(range(1, amount + 1), [None] * amount)}
        self.__cooking_time = {1: 30, 2: 20, 3: 10, 4: 15}
        self.__eating_time = {1: 30, 2: 20, 3: 15, 4: 10}
        self.__cook = Cook()

    def __update(self):
        for n in self.table:
            if n.__update():
                if n.complete:
                    #밖으로 이동
                    return
                n.__change_status(self.__eating_time)

    def empty(self):
        empty = []
        for key in self.table.keys():
            if not self.table[key]:
                empty.append(key)
        return empty

class Cook:
    def __init__(self):
        self.cook = []

    def __update(self):
        pass

class Bill:
    def __init__(self):
        self.__waiting = []
        self.__time = 5

    def new(self, customer: int):
        self.__waiting.append(customer)

    def __update(self):
        self.__time -= 1
        if self.__time < 0:
            self.__time = 5
            self.__waiting.pop(0)
            #문구

