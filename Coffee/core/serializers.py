from django.db import transaction
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

    def validate(self, attrs):
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        if not quantity:
            raise serializers.ValidationError(
                detail='Quantity является обязательнным полем.'
            )
        if price <= 0:
            raise serializers.ValidationError(
                detail='Цена не может быть отрицательной.'
            )
        return super().validate(attrs)


class BaseOrdersSerializer(serializers.ModelSerializer):
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

        read_only_fields = [
            'id',
            'total_price'
        ]

    def validate(self, attrs):
        items = attrs.get('items')
        if not items:
            raise serializers.ValidationError(
                detail='Items не может быть пустым.'
            )
        return super().validate(attrs)

    @staticmethod
    def _create_items(order, items):
        OrdersItems.objects.bulk_create(
            OrdersItems(
                order=order,
                dish=item['dish'],
                price=item['price'],
                quantity=item['quantity']
            ) for item in items
        )


class UpdateOrdersSerializer(BaseOrdersSerializer):

    class Meta(BaseOrdersSerializer.Meta):

        read_only_fields = BaseOrdersSerializer.Meta.read_only_fields + [
            'table_number'
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop('items', [])
        instance.items.all().delete()
        self._create_items(instance, items)
        return super().update(instance, validated_data)


class CreateOrdersSerializer(BaseOrdersSerializer):
    items = OrdersItemsSerializer(
        many=True,
        required=True
    )

    class Meta(BaseOrdersSerializer.Meta):
        read_only_fields = BaseOrdersSerializer.Meta.read_only_fields + [
            'status'
        ]

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop('items', [])
        order = Orders.objects.create(**validated_data)
        self._create_items(order, items)
        return order

