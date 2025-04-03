import pytest
from rest_framework.test import APIClient

from core.models import Orders


@pytest.mark.django_db
def test_orders_content_to_list(many_orders):
    client = APIClient()
    response = client.get('/api/orders/', format='json')
    assert (
        len(response.data) == Orders.objects.all().count()
    ), 'На страницу заказов должны выводиться все существующие заказы'


def test_struct_response_order(order):
    client = APIClient()
    response = client.get('/api/orders/', format='json')
    assert (
        'id' in response.data[0]
    ), 'Ответ на запрос должен содеражть поле id'
    assert (
        'table_number' in response.data[0]
    ), 'Ответ на запрос должен содеражть поле table_number'
    assert (
        'status' in response.data[0]
    ), 'Ответ на запрос должен содеражть поле status'
    assert (
        'items' in response.data[0]
    ), 'Ответ на запрос должен содеражть поле items'
    assert (
        'total_price' in response.data[0]
    ), 'Ответ на запрос должен содеражть поле total_price'


@pytest.mark.django_db
def test_revenue_orders(many_orders):
    client = APIClient()
    response = client.get('/api/orders/revenue/', format='json')
    print(response)
    assert (
        'total_revenue' in response.data
    ), (
        'Ответ должен содержать поле total_revenue',
        'суммой всех оплаченных заказов'
    )
    assert (
        response.data['total_revenue'] == sum(
            order.total_price for order in Orders.objects.filter(
                status='Оплачено'
            )
        )
    ), 'total_revenue должен содержать верное значение.'
    assert (
        len(response.data['results']) == Orders.objects.filter(
            status='Оплачено'
        ).count()
    ), 'Ответ должен содержать все оплаченные заказы.'
