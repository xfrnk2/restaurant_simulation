from collections import namedtuple
from src.restaurant import customer_initialize, waitable

InitializeCase = namedtuple("InitializeTestCase", "customer_num food_num expected")
WaitableCase = namedtuple("WaitableCase", "not_taken_order taken_order expected")

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

def test_waitable():

    cases = (
        WaitableCase(not_taken_order=[5, 10],
                    taken_order=[5, 10, 10],
                     expected=10
                     ),
        WaitableCase(not_taken_order=[7, 9],
                    taken_order=[5, 10, 15],
                    expected=12
                    ),
        WaitableCase(not_taken_order=[],
                     taken_order=[5, 10, 15],
                     expected=0
                     )
    )
    for case in cases:
        taken_order, not_taken_order, expected = case
        assert waitable(taken_order, not_taken_order) == expected
