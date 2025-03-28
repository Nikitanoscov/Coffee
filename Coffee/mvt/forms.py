from django import forms
from django.forms import inlineformset_factory

from core.models import Orders, OrdersItems


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = (
            'table_number',
            'status'
        )


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrdersItems
        fields = (
            'dish',
            'price',
            'quantity'
        )


OrderItemFormSet = inlineformset_factory(
    Orders,
    OrdersItems,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)
