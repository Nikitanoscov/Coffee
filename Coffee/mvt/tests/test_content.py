from django.urls import reverse
import pytest

from core.models import Orders


@pytest.mark.django_db
def test_count_orders_on_list(client, many_orders):
    url = reverse('orders:list')
    response = client.get(url)
    orders = response.context['orders']
    assert (
        orders.count() == Orders.objects.all().count()
    ), (
        'Заказы на главной странице отображаются не корректно:',
        ' количество заказов не соответствует количеству в базе данных'
    )


@pytest.mark.django_db
def test_revenue_orders(client, many_orders):
    url = reverse('orders:revenue')
    response = client.get(url)
    orders = response.context['orders']
    total_sum = response.context['revenue']
    assert (
        orders.count() == Orders.objects.filter(status='Оплачено').count()
    ), (
        'Заказы на странице выручки отображаются не корректно:',
        ' количество заказов не соответствует количеству в базе данных'
    )
    assert (total_sum == sum(
        order.total_price for order in Orders.objects.filter(status='Оплачено')
    )), (
        'Выручка за оплаченные заказы подсчитывается не корректно:',
        ' сумма стоимости заказов не соответствует базе данных'
    )


@pytest.mark.django_db
def test_find_create_form(client):
    url = reverse('orders:create')
    response = client.get(url)
    assert (
        'item_formset' in response.context
    ), 'Страница создания заказов не содержит форму'


@pytest.mark.django_db
def test_find_update_form(client, id_order):
    url = reverse('orders:edit', args=id_order)
    response = client.get(url)
    assert (
        'item_formset' in response.context
    ), 'Страница редактирования заказов не содержит форму'
