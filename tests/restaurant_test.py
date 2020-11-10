from collections import namedtuple
from src.restaurant import customer_initialize, waiting_checker, estimated_waiting_time

InitializeCase = namedtuple("InitializeTestCase", "customer_num food_num expected")
WaitingCase = namedtuple("WaitingCase", "tables waiting_amount waitable_time expected desc")
EstimatedTimeCase = namedtuple("EstimatedTimeCase", "tables waiting_amount expected")
EntranceCase = namedtuple("EntranceCase", "tables, customer_info expected")

def test_customer_initialize():
    cases = (
        InitializeCase(customer_num=3,
                       food_num=1,
                       expected=(3, 1, 30, 30, "스테이크")
                       ),
        InitializeCase(customer_num=1,
                       food_num=2,
                       expected=(1, 2, 20, 20, "스파게티")
                       ),
        InitializeCase(customer_num=3,
                       food_num=4,
                       expected=(3, 4, 10, 15, "그라탱")
                       ),
    )
    for case in cases:
        customer_num, food_num, expected = case
        assert customer_initialize(customer_num, food_num) == expected


def test_waiting_checker():

    cases = (
        WaitingCase(tables=[10, 20, 30],
                    waiting_amount=2,
                    waitable_time=15,
                    expected=False,
                    desc="조건을 만족하는 테이블의 수(1)가 대기인원 수(2)보다 작지 않아 실패"
                    ),
        WaitingCase(tables=[15, 20, 25, 30, 35],
                    waiting_amount=1,
                    waitable_time=20,
                    expected=True,
                    desc="조건을 만족하는 테이블의 수(2)가 대기인원 수(1)보다 크지 않아 실패"
                    ),
        WaitingCase(tables=[15, 21, 23, 30, 37, 40, 45],
                    waiting_amount=1,
                    waitable_time=41,
                    expected=True,
                    desc="조건을 만족하는 테이블의 수(6)가 대기인원 수(1)보다 크지 않아 실패"
                    ),
        WaitingCase(tables=[15, 21, 23, 30, 37, 40, 45],
                    waiting_amount=0,
                    waitable_time=41,
                    expected=True,
                    desc="조건을 만족하는 테이블의 수(6)가 대기인원 수(0)보다 크지 않아 실패"
                    ),
        WaitingCase(tables=[21, 23, 30, 37, 40, 45],
                    waiting_amount=0,
                    waitable_time=15,
                    expected=False,
                    desc="조건을 만족하는 테이블의 수(0)가 대기인원 수(0)보다 작거나 같지 않아 실패"
                    ),
        WaitingCase(tables=[0, 21, 23, 30, 37, 40, 45],
                    waiting_amount=3,
                    waitable_time=21,
                    expected=False,
                    desc="조건을 만족하는 테이블의 수(2)가 대기인원 수(3)보다 작지 않아 실패"
                    ),
    )
    for case in cases:
        tables, waiting_amount, waitable_time, expected, desc = case
        assert waiting_checker(tables, waiting_amount, waitable_time) == expected, desc


def test_estimated_waiting_time():
    cases = (
        EstimatedTimeCase(
            tables=[10, 20, 30],
            waiting_amount=2,
            expected="30분"
        ),
        EstimatedTimeCase(
            tables=[15, 20, 25, 30, 35],
            waiting_amount=1,
            expected="20분"
        ),
        EstimatedTimeCase(
            tables=[21, 23, 30, 37, 40, 45],
            waiting_amount=0,
            expected="21분"
        ),
        EstimatedTimeCase(
            tables=[21, 23, 30, 40, 45],
            waiting_amount=10,
            expected="45분 이상"
        ),
        EstimatedTimeCase(
            tables=[0, 3, 4],
            waiting_amount=2,
            expected="4분"
        ),
        EstimatedTimeCase(
            tables=[0, 1, 3, 4, 5],
            waiting_amount=5,
            expected="5분 이상"
        ),
        EstimatedTimeCase(
            tables=[0, 1, 3, 4, 5, 15],
            waiting_amount=15,
            expected="15분 이상"
        ),
    )

    for case in cases:
        tables, waiting_amount, expected = case
        assert estimated_waiting_time(tables, waiting_amount) == expected

def test_entrance():
    cases = (
        EntranceCase(
            tables=[1, 1, 1, 1, 1, 0, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            customer_info=(3, 1, 30, 30, "스테이크"),
            expected="3번 손님이 6번 테이블에 앉습니다.\n3번 손님이 1번 요리(스테이크)를 주문합니다."
        ),
        EntranceCase(
            tables=[0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            customer_info=(12, 4, 10, 15, "그라탱"),
            expected="12번 손님이 1번 테이블에 앉습니다.\n12번 손님이 4번 요리(그라탱)를 주문합니다."
        )
    )