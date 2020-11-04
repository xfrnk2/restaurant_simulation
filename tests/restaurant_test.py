from collections import namedtuple
from src.restaurant import customer_initialize, waiting_checker

InitializeCase = namedtuple("InitializeTestCase", "customer_num food_num expected")
WaitingCase = namedtuple("WaitingCase", "tables waiting_amount waitable_time expected")

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
        assert customer_initialize(customer_num, food_num)  == expected

def test_waiting_checker():

    cases = (
        WaitingCase(tables=[10, 20, 30],
                    waiting_amount=2,
                    waitable_time=15,
                    expected=False
                     ),
        WaitingCase(tables=[15, 20, 25, 30, 35],
                    waiting_amount=1,
                    waitable_time=20,
                    expected=True
                    ),
        WaitingCase(tables=[15, 21, 23, 30, 37, 40, 45],
                    waiting_amount=1,
                    waitable_time=41,
                    expected=True
                    ),
        WaitingCase(tables=[15, 21, 23, 30, 37, 40, 45],
                    waiting_amount=0,
                    waitable_time=41,
                    expected=True
                    ),
        WaitingCase(tables=[21, 23, 30, 37, 40, 45],
                    waiting_amount=0,
                    waitable_time=15,
                    expected=False
                    ),
        WaitingCase(tables=[15, 21, 23, 30, 37, 40, 45],
                    waiting_amount=3,
                    waitable_time=21,
                    expected=False
                    ),
    )
    for case in cases:
        tables, waiting_amount, waitable_time, expected = case
        assert waiting_checker(tables, waiting_amount, waitable_time) == expected
