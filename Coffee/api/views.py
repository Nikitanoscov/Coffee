from rest_framework.viewsets import ModelViewSet

from core.models import Orders


class Orders(ModelViewSet):
    queryset = Orders.objects.prefetch_related('items')
