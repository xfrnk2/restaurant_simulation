from dataclasses import dataclass
from typing import List
from src.table import Table
from src.customer import Customer, CustomerInfo
import sys
sys.path.append('C:/Users/rad87/Documents/programming/restaurant_simulation')


@dataclass
class TableCase:
    time_data: List[int]
    table = Table

    def init(self):
        self.table = Table(20)
        for i, time in zip(range(1, 21), self.time_data):
            self.table.table[i] = Customer(CustomerInfo(i, i, 0), 0, time)
            self.table.table[i].eating = True
        return self.table


@dataclass
class WaitableCase:
    table: Table
    waitable_time: int
    waiting_amount: int
    expected_table_waitable_time: int
    expected: bool


@dataclass
class UpdateCase:
    table: Table
    expected: List[int]


def test_is_waitable():
    cases = (
        WaitableCase(
            table=TableCase(time_data=range(20, 40)).init(),
            waitable_time=25,
            waiting_amount=3,
            expected_table_waitable_time=0,
            expected=True
        ),
        WaitableCase(
            table=TableCase(time_data=range(20, 40)).init(),
            waitable_time=25,
            waiting_amount=3,
            expected_table_waitable_time=0,
            expected=True
        ),
        WaitableCase(
            table=TableCase(time_data=range(20, 40)).init(),
            waitable_time=22,
            waiting_amount=5,
            expected_table_waitable_time=25,
            expected=False
        ),
        WaitableCase(
            table=TableCase(time_data=range(20, 40)).init(),
            waitable_time=25,
            waiting_amount=30,
            expected_table_waitable_time=39,
            expected=False
        )
    )
    for case in cases:
        table, table_waitable_time, expected = case.table, case.expected_table_waitable_time, case.expected
        waitable_time, waiting_amount = case.waitable_time, case.waiting_amount

        assert table.is_waitable(waitable_time, waiting_amount) == expected
        if not expected:
            assert table.waitable_time == table_waitable_time


def test_update():
    cases = (
        UpdateCase(
            table=TableCase(time_data=[2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]).init(),
            expected=[1, 2, 3]
        ),
        UpdateCase(
            table=TableCase(time_data=[2] * 20).init(),
            expected=[n for n in range(1, 21)]
        ),
        UpdateCase(
            table=TableCase(time_data=[1] * 20).init(),
            expected=[]
        ),
    )

    for case in cases:
        table = case.table

        table.update()
        assert table.update() == case.expected
