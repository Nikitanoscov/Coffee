from rest_framework import serializers

from core.models import Orders, OrdersItems


class OrdersItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdersItems
        fields = (
            'dish',
            'price',
            'quantity'
        )


class WriteOrdersSerializer(serializers.ModelSerializer):
    items = OrdersItemsSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = Orders
        fields = (
            'table_number',
            'items'
        )


class ReadOrdersSerializer(serializers.ModelSerializer):
    items = OrdersItemsSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = Orders
        fields = (
            'id',
            'table_number',
            'status',
            'items',
            'total_price'
        )

