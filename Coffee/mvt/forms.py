from django import forms
from django.forms import inlineformset_factory, ValidationError

from core.models import Orders, OrdersItems


class UpdateOrderForm(forms.ModelForm):
    """
    Форма для редактирования заказа.
    """
    class Meta:
        model = Orders
        fields = (
            'status',
        )


class CreateOrderForm(forms.ModelForm):
    """
    Форма для создания заказа.
    """
    class Meta:
        model = Orders
        fields = (
            'table_number',
        )


class OrderItemForm(forms.ModelForm):
    """
    Форма для создания или редактирования позиции заказа.
    """
    class Meta:
        model = OrdersItems
        fields = (
            'dish',
            'price',
            'quantity'
        )


class ValidateFormSet(forms.BaseInlineFormSet):
    """
    Формсет с дополнительной валидацией для набора форм элементов заказа.
    """
    def clean(self):
        super().clean()
        has_valid_item = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                dish = form.cleaned_data.get('dish')
                price = form.cleaned_data.get('price')
                quantity = form.cleaned_data.get('quantity')
                if dish and price and quantity:
                    has_valid_item = True
        if not has_valid_item:
            raise ValidationError(
                (
                    'Необходимо добавить хотя бы одно блюдо',
                    ' с заполненными всеми полями.'
                )
            )


OrdersItemsFormSet = inlineformset_factory(
    Orders,
    OrdersItems,
    form=OrderItemForm,
    formset=ValidateFormSet,
    extra=1,
    can_delete=True
)
