from src.bill import Bill
from dataclasses import dataclass
from typing import List
import sys
sys.path.append('C:/Users/rad87/Documents/programming/restaurant_simulation')


@dataclass
class updateCase:
    bill = Bill()
    waiting: List[int]
    required_time: int
    expected: List[int]


def test_update():
    '''
    한 손님의 계산이 끝난 시점에서 새로운 손님의 계산이 시작되기까지 생기는 1분의 딜레이를 포함한다.
    즉, 첫번째 손님은 BILLING_CYCLE(5)인 5만큼의 시간이 소요되지만, 그 다음 손님의 차례부터는 앞의 손님의
    계산이 끝나 새롭게 계산을 시작하는 과정이 포함되므로 1분이 딜레이되어,
    BILLING_CYCLE(5)+1 = 6만큼의 시간이 소요된다.

            '''
    cases = (
        updateCase(
                   waiting=[1, 2, 3, 4, 5, 7],
                   required_time=17,
                   expected=[4, 5, 7]),
        updateCase(
                   waiting=[1, 2, 3, 4, 5, 6],
                   required_time=27,
                   expected=[5, 6])
            )
    for case in cases:
        bill, required_time = case.bill, case.required_time
        bill.waiting = case.waiting

        while 0 <= required_time:
            required_time -= 1
            bill.update()

        assert bill.waiting == case.expected
