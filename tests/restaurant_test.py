from dataclasses import dataclass
from src.restaurant import waiting_checker, estimated_waiting_time, table_initialize, \
     available_table, order_initialize, cooks_update, available_new_order, tables_update
import typing


@dataclass()
class WaitingCase:
    tables: typing.List[int]
    waiting_amount: int
    waitable_time: int
    expected: bool
    desc: int


@dataclass()
class EstimatedTimeCase:
    tables: typing.List[int]
    waiting_amount: int
    expected: str


@dataclass()
class EntranceCase:
    customer_num: int
    num: int
    table_num: int
    expected: str


@dataclass()
class TableInitCase:
    customer_num: int
    num: int
    expected: str


@dataclass()
class AvailableTableCase:
    tables: typing.List[int]
    expected: str


@dataclass()
class OrderInitCase:
    customer_num: int
    num: int
    table_idx: int
    expected: str


@dataclass()
class CookedCase:
    customer_num: int
    num: int
    expected: str


@dataclass()
class CooksUpdateCase:
    cooks: typing.List[tuple]
    expected: typing.List[tuple]


@dataclass()
class AvailableNewOrderCase:
    max_cooks_num: int
    cooks_num: int
    new_orders: int
    expected: int


@dataclass()
class TableUpdateCase:
    tables: typing.List[dict]
    expected: tuple


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
        assert waiting_checker(case.tables, case.waiting_amount, case.waitable_time) == case.expected, case.desc


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
        assert estimated_waiting_time(case.tables, case.waiting_amount) == case.expected


def test_table_initialize():
    cases = (
        TableInitCase(
            customer_num=1,
            num=2,
            expected=[20, 20, 1]),
        TableInitCase(
            customer_num=4,
            num=4,
            expected=[10, 10, 4]),
        TableInitCase(
             customer_num=7,
             num=1,
             expected=[30, 30, 7])
            )
    for case in cases:
        assert table_initialize(case.customer_num, case.num) == case.expected


def test_available_table():
    cases = (
        AvailableTableCase(
                           tables={1: 0, 2: 1, 3: 1, 4: 1, 5: 1},
                           expected=[1]
                          ),
        AvailableTableCase(
                           tables={1: 1, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 0, 9: 1},
                           expected=[2, 8]
                          ),
        AvailableTableCase(
                           tables={1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1,
                                   11: 1, 12: 1, 13: 1},
                           expected=[]
                          )

    )
    for case in cases:
        assert available_table(case.tables) == case.expected


def test_order_initialize():
    cases = (
        OrderInitCase(
            customer_num=3,
            num=1,
            table_idx=1,
            expected=[30, 3, 1, 1]),
        OrderInitCase(
            customer_num=1,
            num=2,
            table_idx=1,
            expected=[20, 1, 2, 1]),
        OrderInitCase(
            customer_num=3,
            num=4,
            table_idx=1,
            expected=[15, 3, 4, 1]),
        OrderInitCase(
            customer_num=6,
            num=3,
            table_idx=1,
            expected=[10, 6, 3, 1]),
        )
    for case in cases:
        assert order_initialize(case.customer_num, case.num, case.table_idx) == case.expected


def test_cooks_update():
    cases = (
        CooksUpdateCase(
            cooks=[[1, 3, 1, 3],
                   [5, 5, 4, 0],
                   [10, 2, 3, 2]],
            expected=([[4, 5, 4, 0],
                      [9, 2, 3, 2]],
                      [[0, 3, 1, 3]])),
        CooksUpdateCase(
            cooks=[[1, 3, 1, 6],
                   [1, 5, 4, 5],
                   [10, 2, 3, 4]],
            expected=([[9, 2, 3, 4]],
                      [[0, 3, 1, 6],
                       [0, 5, 4, 5]])),
        CooksUpdateCase(
            cooks=[[5, 3, 1, 6],
                   [6, 5, 4, 5],
                   [10, 2, 3, 4]],
            expected=([[4, 3, 1, 6],
                      [5, 5, 4, 5],
                      [9, 2, 3, 4]], [])),
        CooksUpdateCase(
            cooks=[],
            expected=([], []))
             )
    for case in cases:
        assert cooks_update(case.cooks) == case.expected


def test_available_new_order():
    cases = (
        AvailableNewOrderCase(
            max_cooks_num=3,
            cooks_num=3,
            new_orders=6,
            expected=0
        ),
        AvailableNewOrderCase(
            max_cooks_num=3,
            cooks_num=1,
            new_orders=2,
            expected=2
        ),
        AvailableNewOrderCase(
            max_cooks_num=3,
            cooks_num=2,
            new_orders=2,
            expected=1
        ),
        AvailableNewOrderCase(
            max_cooks_num=3,
            cooks_num=0,
            new_orders=3,
            expected=3
        ),
        AvailableNewOrderCase(
            max_cooks_num=3,
            cooks_num=0,
            new_orders=1,
            expected=1
        )
    )
    for case in cases:
        assert available_new_order(case.max_cooks_num, case.cooks_num, case.new_orders) == case.expected


def test_tables_update():
    cases = (
        TableUpdateCase(
                        tables=[[0, 20, 5],
                                [-1, 25, 2],
                                [21, 25, 4],
                                [20, 20, 8],
                                [30, 30, 7]],
                        expected=([0,
                                   0,
                                   [20, 25, 4],
                                   [20, 20, 8],
                                   [30, 30, 7]],
                                  [5, 2])
                        ),
             )
    for case in cases:
        assert tables_update(case.tables) == case.expected


waiting = [1, 2, 3]
b = {i: table for i, table in zip(range(1, 21), [0]*20)}
print(b)
