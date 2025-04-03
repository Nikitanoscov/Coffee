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
def order_create_form_data():
    return {
        'table_number': 2,
        'items-TOTAL_FORMS': '1',
        'items-INITIAL_FORMS': '0',
        'items-MIN_NUM_FORMS': '0',
        'items-MAX_NUM_FORMS': '1000',
        'items-0-dish': 'Кофе',
        'items-0-price': '100',
        'items-0-quantity': '2',
    }

@pytest.fixture
def order_update_form_data():
    return {
        'status': 'Оплачено',
        'items-TOTAL_FORMS': '1',
        'items-INITIAL_FORMS': '0',
        'items-MIN_NUM_FORMS': '0',
        'items-MAX_NUM_FORMS': '1000',
        'items-0-dish': 'Кофе',
        'items-0-price': '100',
        'items-0-quantity': '2',
    }
