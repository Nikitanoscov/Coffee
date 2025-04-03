from django.db import transaction
from rest_framework import serializers

from core.models import Orders, OrdersItems


class OrdersItemsSerializer(serializers.ModelSerializer):
    """
    Сериализатор блюд для вложенного использования при работе с заказами.
    """
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
    """
    Базовый класс для наследования сериализаторов для работы с заказами.
    """
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
        dish_names = [item['dish'] for item in items]
        if len(dish_names) != len(set(dish_names)):
            raise serializers.ValidationError(
                detail='В одном заказе не может быть двух одинаковых блюд.'
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
    """
    Сериализатор для редактирования заказов.
    """
    class Meta(BaseOrdersSerializer.Meta):

        read_only_fields = BaseOrdersSerializer.Meta.read_only_fields + [
            'table_number'
        ]

    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError(
                'status является обязательным полем'
            )
        return super().validate(attrs)

    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop('items', [])
        instance.items.all().delete()
        self._create_items(instance, items)
        return super().update(instance, validated_data)


class CreateOrdersSerializer(BaseOrdersSerializer):
    """
    Сериализатор для сохдания заказов.
    """
    items = OrdersItemsSerializer(
        many=True,
        required=True
    )

    class Meta(BaseOrdersSerializer.Meta):
        read_only_fields = BaseOrdersSerializer.Meta.read_only_fields + [
            'status'
        ]

    def validate(self, attrs):
        if 'table_number' not in attrs:
            raise serializers.ValidationError(
                'table_number является обязательным полем'
            )
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop('items', [])
        order = Orders.objects.create(**validated_data)
        self._create_items(order, items)
        return order
