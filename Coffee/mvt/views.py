from django.forms import inlineformset_factory

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import OrderForm, OrderItemForm, OrderItemFormSet
from core.models import Orders, OrdersItems


def redirect_to_list(request):
    return redirect('orders:orders-list')


class OrderListView(ListView):
    """
    Класс-представление для отображения списка заказов.
    """
    model = Orders
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'


class OrderCreateView(CreateView):
    """
    Класс-представление для создания нового заказа.
    """
    model = Orders
    form_class = OrderForm
    template_name = 'orders/orders_create.html'
    success_url = reverse_lazy('orders:orders-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = OrderItemFormSet(
                self.request.POST
            )
        else:
            context['item_formset'] = OrderItemFormSet(
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


class OrderDetailView(DeleteView):
    model = Orders
    template_name = 'orders/orders_detail.html'
