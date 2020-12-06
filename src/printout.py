

class PrintOut:
    @staticmethod
    def init():
        __class__.__queue = []
        __class__.__messages = {
            'arrive': 'f"{info[0]}번째 손님이 시각 {info[1]}분에 레스토랑에 도착했습니다."',
            'back': 'f"손님이 기다릴 수 없어 돌아갑니다. 현재 대기 시간 {info[0]} / 대기 가능 시간 {info[1]}"',
            'order_request': 'f"{info[0]}번 손님이 {info[1]}번 테이블에 앉습니다. {info[0]}번 손님이 {info[2]}번 요리({__class__.food_name[info[2]]})를 주문합니다."',
            'start': 'f"{info[0]}번 손님의 {info[2]}번 요리({__class__.food_name[info[2]]}) 조리가 끝났습니다. {info[0]}번 손님이 식사를 시작합니다."',
            'finish': 'f"{info}번 손님이 식사를 마쳤습니다. {info}번 손님이 계산대 앞에 줄을 섭니다."',
            'leave': 'f"{info}번 손님이 계산을 마치고 레스토랑을 떠났습니다."',
            'now': 'f"[현재시각 : {info}분]"'
            }

    @staticmethod
    def add(sign: str, info: tuple or int):
        __class__.__queue.append((sign, info))

    @staticmethod
    def printout():
        if not __class__.__queue:
            return

        for sign, info in __class__.__queue:
            print(eval(__class__.__messages[sign]))
        __class__.__queue = []

    __queue = []
    __messages = {}
    food_name = {1: "스테이크", 2: "스파게티", 3: "마카로니", 4: "그라탱"}
