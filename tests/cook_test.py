from src.cook import Cook
from dataclasses import dataclass


@dataclass
class CookCase:
    order_time: list
    cooks_time: list
    cook: Cook
    expected: int


def test_cook_waiting_time():
    cases = (
        CookCase(order_time=[],
                 cooks_time=[],
                 cook=Cook(),
                 expected=0
                 ),
        CookCase(order_time=[],
                 cooks_time=[5, 10, 15],
                 cook=Cook(),
                 expected=0
                 ),
        CookCase(order_time=[5, 10, 15],
                 cooks_time=[5, 10, 15],
                 cook=Cook(),
                 expected=15
                 ),
        CookCase(order_time=[10],
                 cooks_time=[20, 30, 40],
                 cook=Cook(),
                 expected=30
                 ),
            )
    for case in cases:
        cook = case.cook
        cook.order_time, cook.cooks_time = case.order_time, case.cooks_time
        assert cook.waiting_time() == case.expected


def test_available_new_order():
    cases = (
        CookCase(
            order_time=[1],
            cooks_time=[1, 1],
            cook=Cook(),
            expected=1
        ),
        CookCase(
             order_time=[1, 1, 1],
             cooks_time=[1, 1],
             cook=Cook(),
             expected=1
         ),
        CookCase(
             order_time=[],
             cooks_time=[1, 1],
             cook=Cook(),
             expected=0
         ),
        CookCase(
             order_time=[1, 1, 1],
             cooks_time=[1],
             cook=Cook(),
             expected=2
         )
             )

    for case in cases:
        cook = case.cook
        cook.order_time, cook.cooks_time = case.order_time, case.cooks_time
        assert cook.available_new_order() == case.expected
