from restaurant_simulation.src.restaurant import CustomerInfo, Restaurant
from restaurant_simulation.src.customer import Customer

visiting_period = 5
restaurant = Restaurant(visiting_period)

def test_customer_visiting():
    customer = restaurant.customer_visiting(0)
    assert isinstance(customer, Customer), "리턴값이 Customer 클래스의 인스턴스가 아님"
    assert customer.info.number % visiting_period == 0, "방문 주기에 맞게 손님이 방문하지 않음"
test_customer_visiting()