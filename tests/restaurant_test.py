from collections import namedtuple
from src.restaurant import customer_initialize

Case = namedtuple("TestCase", "customer_num food_num expected")
CustomerInfo = namedtuple("CustomerInfo", "customer_num food_num eating_time cooking_time")

def test_customer_initialize():
    cases = (
        Case(customer_num=3,
             food_num=1,
             expected=(3, 1, 30, 30, "스테이크")
             ),
        Case(customer_num=1,
             food_num=2,
             expected=(1, 2, 20, 20, "스파게티")
             ),
        Case(customer_num=3,
             food_num=4,
             expected=(3, 4, 10, 15, "그라탱")
             ),
    )
    for case in cases:
        customer_num, food_num, expected = case
        assert customer_initialize(customer_num, food_num)  == expected
