from src.bill import Bill
import pytest


@pytest.fixture
def bill():
    mock = Bill()
    mock.waiting = [1, 2, 3, 4, 5, 6]
    mock.time = 0
    return mock


def test_update(bill):
    bill.update()
    assert bill.time == 5 and bill.waiting == [2, 3, 4, 5, 6]
