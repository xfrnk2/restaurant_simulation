from collections import namedtuple
from src.restaurant import waiting_checker, estimated_waiting_time, entrance, table_initialize, \
    available_table, order_initialize

CustomerInitCase = namedtuple("CustomerInitCase", "customer_num food_num expected")
WaitingCase = namedtuple("WaitingCase", "tables waiting_amount waitable_time expected desc")
EstimatedTimeCase = namedtuple("EstimatedTimeCase", "tables waiting_amount expected")
EntranceCase = namedtuple("EntranceCase", "customer_info table_idx expected")
TableInitCase = namedtuple("TableInitCase", "customer_num num expected")
AvailableTableCase = namedtuple("AvailableTableCase", "tables expected")
OrderInitCase = namedtuple("OrderInitCase", "customer_num num table_idx expected")
CookedCase = namedtuple("CookedCase", "customer_num num expected")

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
            customer_info=(3, 1, 30, 30, "스테이크"),
            table_idx=6,
            expected="3번 손님이 7번 테이블에 앉습니다.\n3번 손님이 1번 요리(스테이크)를 주문합니다."
        ),
        EntranceCase(
            customer_info=(12, 4, 10, 15, "그라탱"),
            table_idx=7,
            expected="12번 손님이 8번 테이블에 앉습니다.\n12번 손님이 4번 요리(그라탱)를 주문합니다."
        )
    )

    for case in cases:
        customer_info, table_idx, expected = case
        assert entrance(customer_info, table_idx) == expected


def test_table_initialize():
    cases = (TableInitCase(
        customer_num=1,
        num=2,
        expected={"is_eating": False, "eating_time": 20, "customer_num": 1}
            ),
        TableInitCase(
            customer_num=4,
            num=4,
            expected={"is_eating": False, "eating_time": 10, "customer_num": 4}
            ),
        TableInitCase(
             customer_num=7,
             num=1,
             expected={"is_eating": False, "eating_time": 30, "customer_num": 7}
           )
    )

    for case in cases:
        customer_num, num, expected = case
        assert table_initialize(customer_num, num) == expected


def test_available_table():
    cases = (
        AvailableTableCase(
                           tables=[0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                                   1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                           expected=0
                          ),
        AvailableTableCase(
                           tables=[1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                                   1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                           expected=7
                          )
    )

    for case in cases:
        tables, expected = case
        assert available_table(tables) == expected


def test_order_initialize():
    cases = (
        OrderInitCase(
            customer_num=3,
            num=1,
            table_idx=1,
            expected=[30, {"customer_num": 3, "num": 1, "table_idx": 1}]),
        OrderInitCase(
            customer_num=1,
            num=2,
            table_idx=1,
            expected=[20, {"customer_num": 1, "num": 2, "table_idx": 1}]),
        OrderInitCase(
            customer_num=3,
            num=4,
            table_idx=1,
            expected=[15, {"customer_num": 3, "num": 4, "table_idx": 1}]),
        OrderInitCase(
            customer_num=6,
            num=3,
            table_idx=1,
            expected=[10, {"customer_num": 6, "num": 3, "table_idx": 1}]),
        )

    for case in cases:
        customer_num, num, table_idx, expected = case
        assert order_initialize(customer_num, num, table_idx) == expected

def test_cooked():
    cases = (
        CookedCase(customer_num=5,
                   num=2,
                   expected="5번 손님의 2번 요리(스파게티) 조리가 끝났습니다.\n5번 손님이 식사를 시작합니다."),
        CookedCase(customer_num=3,
                   num=4,
                   expected="3번 손님의 4번 요리(그라탱) 조리가 끝났습니다.\n3번 손님이 식사를 시작합니다.")
            )

    for case in cases:
        customer_num, num, expected = case
        assert cooked(customer_num, num) == expected
