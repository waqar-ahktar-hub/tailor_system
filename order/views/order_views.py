"""Views for order application."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import View

from client.models import Client
from order.forms import OrderForm
from order.models import Order, Task


class OrderListView(LoginRequiredMixin, View):
    """Class based view for Order for listing all the orders."""

    def get(self, request):
        """Render order list template.."""
        orders = Order.objects.exclude(status=Order.CLOSED)
        context = {
            'orders': orders,
        }
        return render(request, 'order/list-orders.html', context)


order_list_view = OrderListView.as_view()


class OrderDetailView(LoginRequiredMixin, View):
    """Class based view for Order for detail of order."""

    def get(self, request, id):
        """Render order detail tempalte.."""
        order = Order.objects.get(id=id)
        tasks = Task.objects.filter(order=order)
        context = {
            'order': order,
            'tasks': tasks
        }
        return render(request, 'order/order-detail.html', context)


order_detail_view = OrderDetailView.as_view()


class OrderAddView(LoginRequiredMixin, View):
    """Class based view for adding new order."""

    def get(self, request, client_id):
        """Return add new order form."""
        client = get_object_or_404(Client, id=client_id)
        form = OrderForm()
        return render(request, 'order/add-order.html',
                      {'form': form, 'func': 'Add', 'client': client})

    def post(self, request, client_id):
        """Save order and redirect to order list."""
        form = OrderForm(request.POST)
        client = get_object_or_404(Client, id=client_id)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.client = client
            new_order.save()
            return redirect('order:orders')
        else:
            return render(request, 'order/add-order.html', {'form': form, 'func': 'Add', 'client': client})


order_add_view = OrderAddView.as_view()


class OrderUpdateView(LoginRequiredMixin, View):
    """Class based view for updating new order."""

    def get(self, request, id):
        """Return add new order form."""
        order = get_object_or_404(Order, id=id)
        form = OrderForm(instance=order)
        return render(request, 'order/add-order.html',
                      {'form': form, 'func': 'Update', 'order': order})

    def post(self, request, id):
        """Save order and redirect to order list."""
        order = get_object_or_404(Order, id=id)
        client = get_object_or_404(Client, id=order.client.id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.client = client
            new_order.save()
            return redirect('order:orders')
        else:
            return render(request, 'order/add-order.html', {'form': form, 'func': 'Update', 'order': order})


order_update_view = OrderUpdateView.as_view()
