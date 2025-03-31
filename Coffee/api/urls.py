from django.urls import include, path
from rest_framework import routers

from .views import OrdersViewSet, RevenueView

router = routers.DefaultRouter()
router.register(r'orders', OrdersViewSet, basename='order')

urlpatterns = [
    path(
        'orders/revenue/',
        RevenueView.as_view()
    ),
    path('', include(router.urls)),
]
