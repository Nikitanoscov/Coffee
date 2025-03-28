from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path(
        '',
        views.redirect_to_list
    ),
    path(
        'orders/',
        views.OrderListView.as_view(),
        name='orders-list'
    ),
    path(
        'orders/create/',
        views.OrderCreateView.as_view(),
        name='orders-create'
    ),
    path(
        'orders/<int:order_id>/',
        views.OrderDetailView.as_view(),
        name='orders-detail'
    ),
]
