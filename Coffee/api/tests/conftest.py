import pytest

from core.models import Orders, OrdersItems


@pytest.fixture
def order(db):
    order = Orders.objects.create(
        table_number=1
    )
    OrdersItems.objects.create(
        order=order,
        dish='Ватрушки',
        price=250,
        quantity=3
    )
    return order


@pytest.fixture
def id_order(order):
    return (order.id,)


@pytest.fixture
def many_orders(db):
    orders = []
    for i in range(1, 4):
        order = Orders.objects.create(
            table_number=i,
            status='Оплачено'
        )
        OrdersItems.objects.create(
            order=order,
            dish=f'Блюдо {i}',
            price=i * 10,
            quantity=1
        )
        orders.append(order)
    return orders


@pytest.fixture
def create_data():
    return {
        "table_number": 7,
        "items": [
            {
                "dish": "Ватрушки",
                "price": 125,
                "quantity": 3
            },
        ]
    }


@pytest.fixture
def update_data():
    return {
        "status": "Оплачено",
        "items": [
            {
                "dish": "Капучино",
                "price": 256,
                "quantity": 3
            },
            {
                "dish": "Ванильное мороженное",
                "price": 99,
                "quantity": 3
            }
        ]
    }
