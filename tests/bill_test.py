from src.bill import Bill
import pytest
import sys
sys.path.append('C:/Users/rad87/Documents/programming/restaurant_simulation')


@pytest.fixture
def bill():
    mock = Bill()
    mock.waiting = [1, 2, 3, 4, 5, 6]
    mock.time = 0
    return mock


def test_update(bill):
    bill.update()
    assert bill.time == 5 and bill.waiting == [2, 3, 4, 5, 6]
