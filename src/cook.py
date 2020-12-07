

class Cook:
    def __init__(self):

        self.order_time = []
        self.cooks_time = []

    def waiting_time(self):
        result = 0
        '''
        요리사가 지정된 테이블에 앉은 손님의 주문을 배정받아 조리를 시작하기 전까지의 소요시간을 반환합니다.
        대기주문이 있는지 확인하여 없으면 0을 반환합니다.
        order_time : 대기 주문별 조리에 소요되는 시간을 담고 있는 리스트
        cooks_time : 요리중인 요리사의 남은 조리시간을 담고 있는 리스트
        '''

        if self.order_time:
            order_time, cooks_time = self.order_time, self.cooks_time

            # 일하고 있는 요리사가 있으면 그중 가장 적은 시간을 반환하기 위한 연산을 1회 수행하기 위해 0을 추가합니다.
            order_time.append(0)

            while order_time and cooks_time:
                # 일하고 있는 요리사의 시간 중 가장 적은 시간을 target_time 변수로 할당합니다.
                cooks_time.sort()
                target_time = cooks_time.pop(0)

                # 소요시킬 소요시간(target_time)을 결과에 더합니다.
                result += target_time

                # 소요시킬 소요시간만큼 리스트 내 모든 원소의 값을 감소시켜 0을 만듭니다.
                cooks_time = list(map(lambda cook_time: cook_time - target_time, cooks_time))

                # 대기 주문중 우선순위가 가장 높은 주문을 요리중이 아닌 요리사에게 배정시킵니다.
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
