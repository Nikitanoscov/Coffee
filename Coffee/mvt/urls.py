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
        name='list'
    ),
    path(
        'orders/create/',
        views.OrderCreateView.as_view(),
        name='create'
    ),
    path(
        'orders/<int:order_id>/delete',
        views.delete_order,
        name='delete'
    ),
    path(
        'orders/<int:order_id>/edit/',
        views.OrderUpdateView.as_view(),
        name='edit'
    ),
    path(
        'orders/<int:order_id>/',
        views.OrderDetailView.as_view(),
        name='detail'
    ),
    path(
        'orders/revenue/',
        views.RevenueGetView.as_view(),
        name='revenue'
    )
]
