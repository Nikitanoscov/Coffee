from http import HTTPStatus

from django.urls import reverse
import pytest

from core.models import Orders


@pytest.mark.django_db
def test_user_can_create_order(client, order_create_form_data):
    url = reverse('orders:create')
    count_orders = Orders.objects.all().count()
    client.post(url, data=order_create_form_data)
    assert (
        count_orders + 1 == Orders.objects.all().count()
    ), 'Заказ с валидными данными должен быть создан'
    new_order = Orders.objects.get()
    assert (
        new_order.table_number == order_create_form_data['table_number']
    ), 'При создании заказа указываться не верный table_number'
    assert (
        new_order.status == 'В ожидании'
    ), 'Поле status по умолчанию должно иметь значение "В ожидании"'
    assert (
        new_order.items.all().count() == 1
    ), 'Блюда для заказа сохраняются не корректно'


@pytest.mark.django_db
def test_user_cant_create_order_with_bad_order_data(
    client,
    order_create_form_data
):
    order_create_form_data.pop('table_number')
    url = reverse('orders:create')
    count_orders = Orders.objects.all().count()
    client.post(url, data=order_create_form_data)
    assert (
        Orders.objects.all().count() == count_orders
    ), 'Заказ не может быть создан без поля table_number'


@pytest.mark.django_db
def test_user_cant_create_order_with_bad_items_data(
    client,
    order_create_form_data
):
    order_create_form_data.pop('items-0-dish')
    url = reverse('orders:create')
    count_orders = Orders.objects.all().count()
    client.post(url, data=order_create_form_data)
    assert (
        Orders.objects.all().count() == count_orders
    ), 'Заказ не может быть создан без поля item_dish'


@pytest.mark.django_db
def test_user_can_delete_order(client, id_order):
    url = reverse('orders:delete', args=id_order)
    count_order = Orders.objects.all().count()
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert (
        Orders.objects.all().count() == count_order - 1
    ), 'При удалении заказ должен удалятся из базы данных'


@pytest.mark.django_db
def test_user_can_update_order_status(
    client,
    id_order,
    order_update_form_data
):
    url = reverse('orders:edit', args=id_order)
    count_orders = Orders.objects.filter(status='Оплачено').count()
    client.post(url, data=order_update_form_data)
    assert (
        count_orders + 1 == Orders.objects.filter(status='Оплачено').count()
    ), (
        'При редактировании статуса заказа,',
        ' не происходит изменение данных в базе'
    )
