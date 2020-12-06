from src.customer import Customer, CustomerInfo
import sys
import pytest
sys.path.append('C:/Users/rad87/Documents/programming/restaurant_simulation')

first_cases = (
    (CustomerInfo(2, 3, 4), 0, 10),
    (CustomerInfo(4, 5, 1), 0, 30),
              )

second_cases = (
    (CustomerInfo(4, 5, 1), 29, 30),
    (CustomerInfo(5, 6, 7), 50, 40),
    (CustomerInfo(1, 2, 3), 25, 9),
    (CustomerInfo(1, 2, 3), 25, 0),
                )


@pytest.mark.parametrize("info,eating_time,total_time", (*first_cases, *second_cases))
def test_customer_init(info, eating_time, total_time):
    assert Customer(info, eating_time, total_time).time == total_time
    assert Customer(info, eating_time, total_time).info == info
    assert not Customer(info, eating_time, total_time).dish


@pytest.mark.parametrize("info,eating_time,total_time", first_cases)
def test_customer_update(info, eating_time, total_time):
    customer = Customer(info, eating_time, total_time)
    customer.update()
    customer.update()
    assert not customer.dish


@pytest.mark.parametrize("info,eating_time,total_time", second_cases)
def test_customer_update2(info, eating_time, total_time):
    customer = Customer(info, eating_time, total_time)
    customer.update()
    customer.update()
    assert customer.dish
