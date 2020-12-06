from collections import namedtuple
from dataclasses import dataclass
from src.table import Table
CustomerInfo = namedtuple('CustomerInfo', 'number, table, food')
table = Table(20)

@dataclass()
class WaitableCase:
    table: dict
    waitable_time: int
    waiting_amount: int
