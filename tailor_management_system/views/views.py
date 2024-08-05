"""Views for tailor management system application."""

import collections
import json
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views import View

from client.models import Client
from order.models import Order, Task
from product.models import Product, ProductImages


class DashboardView(LoginRequiredMixin, View):
    """Dashboard class based view."""

    def get(self, request):
        """Dashboard view."""
        # No of orders against each order status
        orders_by_status_groups = Order.objects.all().values('status').annotate(total=Count('status'))
        order_stats = {di['status']: di['total'] for di in orders_by_status_groups}
        order_stats['total'] = sum(order_stats.values())

        # No of times each product is sold
        orders_by_product_groups = Order.objects.all().values('product').annotate(total=Count('product'))
        product_stats = {di['product']: di['total'] for di in orders_by_product_groups}
        product_stats.pop(None, None)

        # Product image against each product
        product_images_dict = {}
        for product_id, _ in product_stats.items():
            product = Product.objects.get(id=product_id)
            product_images = ProductImages.objects.filter(product=product).first()
            if product_images:
                product_images_dict[product_id] = product_images

        # 8 tasks with recently upcoming deadlines
        product_stats[0] = Order.objects.filter(product_id__isnull=True) .count()
        sorted_product_stats = sorted(product_stats.items(), key=lambda kv: kv[1], reverse=True)
        ordered_product_stats = collections.OrderedDict(sorted_product_stats)
        tasks = Task.objects.exclude(order__status=Order.CLOSED).exclude(
            status=Task.COMPLETED).order_by('deadline__month', 'deadline__day')

        # Top 5 recently added clients
        clients = Client.objects.order_by('-creation_date')[:5]

        # No of orders recieved in each of last 15 days for Daily Orders chart
        today = datetime.today()
        date_of_sixteen_days_ago = datetime.today() - timedelta(days=10)
        orders_from_last_sixteen_days = Order.objects.filter(date_recieved__gt=date_of_sixteen_days_ago)
        orders_by_date = orders_from_last_sixteen_days.values('date_recieved').annotate(total=Count('date_recieved'))
        order_date_count_dict = {dic['date_recieved']: dic['total'] for dic in orders_by_date}
        dates_for_orders = order_date_count_dict.keys()
        for d in (datetime.today() - timedelta(days=x) for x in range(0, 10)):
            if d.date() not in dates_for_orders:
                order_date_count_dict[d.date()] = 0.9

        sorted_orders_by_date = sorted(order_date_count_dict.items(), key=lambda kv: kv[0])
        sorted_dates_against_orders = collections.OrderedDict(sorted_orders_by_date)
        dates = [str(d) for d, _ in sorted_dates_against_orders.items()]
        no_of_orders = [no_of_orders for _, no_of_orders in sorted_dates_against_orders.items()]

        # No of orders by product type for Product Type Chart
        custom_orders_count = custom_orders_count_percentage = product_based_count = product_based_count_percentage = 0
        if order_stats.get('total') > 0:
            custom_orders_count = product_stats.get(0)
            product_based_count = order_stats.get('total') - custom_orders_count
            custom_orders_count_percentage = round((custom_orders_count/order_stats.get('total')) * 100, 2)
            product_based_count_percentage = round((product_based_count/order_stats.get('total')) * 100, 2)

        # Task completion percentage chart.
        completed_tasks_of_pending_orders = Task.objects.exclude(
            order__status=Order.CLOSED
        ).filter(status=Task.COMPLETED).count()
        pending_task_percentage = completed_task_percentage = 0
        total_tasks_against_pending_orders = Task.objects.exclude(order__status=Order.CLOSED).count()
        if total_tasks_against_pending_orders > 0:
            pending_task_percentage = round((tasks.count()/total_tasks_against_pending_orders) * 100, 2)
            completed_task_percentage = round(
                (completed_tasks_of_pending_orders/total_tasks_against_pending_orders) * 100, 2
            )

        # Sales per month chart.
        sales_of_this_year = Order.objects.filter(date_recieved__year=datetime.today().year)
        sales_by_month = sales_of_this_year.annotate(
            month=TruncMonth('date_recieved')
            ).values('month').annotate(total=Count('id'))
        sales_by_month_dict = {dic['month']: dic['total'] for dic in sales_by_month}
        months = [date.month for date in sales_by_month_dict.keys()]
        for i in range(1, datetime.today().month + 1):
            if i not in months:
                sales_by_month_dict[datetime.today().replace(month=i).date()] = 0

        sorted_sales_by_month_dict = sorted(sales_by_month_dict.items(), key=lambda kv: kv[0])
        sales_per_month = collections.OrderedDict(sorted_sales_by_month_dict)
        month_names = [d.strftime('%B') for d, _ in sales_per_month.items()][2:]
        sales_each_month = [s for _, s in sales_per_month.items()][2:]

        context = {
            'order_stats': order_stats,
            'product_stats': ordered_product_stats,
            'product_images': product_images_dict,
            'tasks': tasks[:8],
            'clients': clients,
            'order_dates': json.dumps(dates),
            'order_count_against_dates': json.dumps(no_of_orders),
            'custom_orders_count': custom_orders_count,
            'product_based_count': product_based_count,
            'custom_orders_count_percentage': custom_orders_count_percentage,
            'product_based_count_percentage': product_based_count_percentage,
            'pending_tasks': tasks.count(),
            'completed_tasks': completed_tasks_of_pending_orders,
            'completed_task_percentage': completed_task_percentage,
            'pending_task_percentage': pending_task_percentage,
            'month_names': json.dumps(month_names),
            'sales_each_month': json.dumps(sales_each_month)
        }
        return render(request, 'tailor_management_system/dashboard.html', context)


dashboard_view = DashboardView.as_view()
