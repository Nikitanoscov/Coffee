from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CreateOrderForm, OrdersItemsFormSet, UpdateOrderForm
from core.models import Orders, OrdersItems


def redirect_to_list(request):
    """
    Функция для редиректа с страницы без префикса.
    """
    return redirect('orders:list')


class OrderListView(ListView):
    """
    Класс-представление для отображения списка заказов.
    """
    model = Orders
    queryset = Orders.objects.prefetch_related('items')
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        order_id = self.request.GET.get('order_id')
        if status:
            queryset = queryset.filter(status=status)
        if order_id:
            queryset = queryset.filter(id=order_id)
        return queryset


class OrderCreateView(CreateView):
    """
    Класс-представление для создания нового заказа.
    """
    model = Orders
    form_class = CreateOrderForm
    template_name = 'orders/orders_create.html'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = OrdersItemsFormSet(
                self.request.POST
            )
        else:
            context['item_formset'] = OrdersItemsFormSet(
                queryset=OrdersItems.objects.none()
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            self.object = form.save()
            items = item_formset.save(commit=False)
            for item in items:
                item.order = self.object
                item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class OrderUpdateView(UpdateView):
    """
    Класс-представление для редактирования существующего заказа.
    """
    model = Orders
    form_class = UpdateOrderForm
    template_name = 'orders/orders_update.html'
    success_url = reverse_lazy('orders:list')
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = OrdersItemsFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context['item_formset'] = OrdersItemsFormSet(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            self.object = form.save()
            items = item_formset.save(commit=False)
            for item in item_formset.deleted_objects:
                item.delete()
            for item in items:
                item.order = self.object
                item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class RevenueGetView(ListView):
    """
    Класс представления для отображения оплаченных заказов и выручки за них
    """
    template_name = 'orders/order_revenue.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Orders.objects.prefetch_related(
            'items'
        ).filter(
            status='Оплачено'
        )

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['revenue'] = sum(
            order.total_price for order in self.get_queryset()
        )
        return result


def delete_order(request, order_id):
    """
    Функция для удаления заказа без использования шаблона.
    """
    order = get_object_or_404(
        Orders,
        id=order_id
    )
    order.delete()
    return redirect('orders:list')
