import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Orders


@pytest.mark.django_db
def test_user_can_create_order(create_data):
    client = APIClient()
    count_orders = Orders.objects.all().count()
    response = client.post('/api/orders/', create_data, 'json')
    new_order = Orders.objects.get()
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), 'При вводе корректных данных должен возращать статус 201'
    assert count_orders + 1 == Orders.objects.all().count()
    assert (
        new_order.table_number == create_data['table_number']
    ), 'При создании заказа указываться не верный table_number'
    assert (
        new_order.status == 'В ожидании'
    ), 'Поле status по умолчанию должно иметь значение "В ожидании"'
    assert (
        new_order.items.all().count() == 1
    ), 'Блюда для заказа сохраняются не корректно'


@pytest.mark.django_db
def test_user_cant_create_order_with_bad_order_data(create_data):
    client = APIClient()
    create_data.pop('table_number')
    count_orders = Orders.objects.all().count()
    response = client.post('/api/orders/', create_data, 'json')
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), (
        'Ответ на запрос содержащий не корректные данные',
        ' должен возвращаться со статусом 400'
    )
    assert (
        Orders.objects.all().count() == count_orders
    ), 'Заказ не может быть создан без поля table_number'


@pytest.mark.django_db
def test_user_cant_create_order_with_bad_items_data(create_data):
    client = APIClient()
    create_data['items'][0].pop('dish')
    count_orders = Orders.objects.all().count()
    response = client.post('/api/orders/', create_data, 'json')
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), (
        'Ответ на запрос содержащий не корректные данные',
        ' должен возвращаться со статусом 400'
    )
    assert (
        Orders.objects.all().count() == count_orders
    ), 'Заказ не может быть создан без поля item_dish'


@pytest.mark.django_db
def test_user_can_delete_order(order):
    client = APIClient()
    count_order = Orders.objects.all().count()
    response = client.delete(f'/api/orders/{order.id}/')
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), 'Ответ на удаление заказа должен возвращаться со статусом 204'
    assert (
        Orders.objects.all().count() == count_order - 1
    ), 'При удалении заказ должен удалятся из базы данных'


@pytest.mark.django_db
def test_user_can_update_order_status(order, update_data):
    client = APIClient()
    count_orders = Orders.objects.filter(status=update_data['status']).count()
    response = client.put(f'/api/orders/{order.id}/', update_data, 'json')
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Ответ на редактирование заказа должен возвращаться со статусом 200'
    assert (
        count_orders + 1 == Orders.objects.filter(
            status=update_data['status']
        ).count()
    ), (
        'При редактировании статуса заказа,',
        ' не происходит изменение данных в базе'
    )
