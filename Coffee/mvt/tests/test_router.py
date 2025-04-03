from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('orders:list', None),
        ('orders:revenue', None),
        ('orders:create', None),
        ('orders:edit', lazy_fixture('id_order'))
    ),
)
def test_page_accessibility(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert (
        response.status_code == HTTPStatus.OK
    ), f'Нет доступа к странице {name}'
