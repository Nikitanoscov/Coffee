from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import SAFE_METHODS
from django.db.models import Sum

from core.models import Orders
from core.serializers import UpdateOrdersSerializer, CreateOrdersSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.prefetch_related('items')
    serializer_class = CreateOrdersSerializer
    filterset_fields = ['id', 'status']

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateOrdersSerializer
        return super().get_serializer_class()


class RevenueView(ListAPIView):
    queryset = Orders.objects.prefetch_related(
        'items'
    ).filter(
        status='Оплачено'
    )
    serializer_class = CreateOrdersSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_revenue = sum(order.total_price for order in queryset)
        serializer_data = self.get_serializer(
            queryset,
            many=True
        ).data
        return Response({
            'results': serializer_data,
            'total_revenue': total_revenue
        })
