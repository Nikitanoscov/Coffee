import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_list_url_availability():
    client = APIClient()
    response = client.get('/api/orders/')
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Не корректный статус ответа на запрос.'


@pytest.mark.django_db
def test_edit_url_availability(order, update_data):
    client = APIClient()
    response = client.put(
        f'/api/orders/{order.id}/',
        data=update_data,
        format='json'
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Не корректный статус ответа на запрос.'


@pytest.mark.django_db
def test_create_url_availability(create_data):
    client = APIClient()
    response = client.post('/api/orders/', data=create_data, format='json')
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), 'Не корректный статус ответа на запрос.'


@pytest.mark.django_db
def test_revenue_url_availability():
    client = APIClient()
    response = client.get('/api/orders/revenue/')
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Не корректный статус ответа на запрос.'
