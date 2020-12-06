from src.customer import Customer, CustomerInfo
import pytest
import sys
sys.path.append('C:/Users/rad87/Documents/programming/restaurant_simulation')


@pytest.fixture
def customer():
    return Customer(CustomerInfo(2, 3, 4), 0, 40)


@pytest.fixture
def customer_update_cases():
    cases = [Customer(CustomerInfo(2, 3, 4), 0, 40),
             Customer(CustomerInfo(5, 6, 7), 50, 40)
             ]

    another_case = Customer(CustomerInfo(8, 9, 10), 1, 25)
    another_case.update()

    return *cases, another_case


def test_customer_init(customer):

    assert customer.time == 40
    assert customer.info == (2, 3, 4)
    assert not customer.dish


def test_customer_update(customer_update_cases):
    for case in customer_update_cases:
        case.update()
        if case.time <= case.eating_time:
            assert case.dish
        else:
            assert not case.dish
