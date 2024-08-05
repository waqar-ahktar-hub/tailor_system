"""urls for order application."""

from django.urls import path

from order.views.order_views import order_add_view, order_detail_view, order_list_view, order_update_view
from order.views.task_views import task_add_view, task_delete_view, task_detail_view, task_list_view, task_update_view

app_name = 'order'

urlpatterns = [
    path('orders/', order_list_view, name='orders'),
    path('order/<int:id>/', order_detail_view, name='order_detail'),
    path('order/add/<int:client_id>/', order_add_view, name='order_add'),
    path('order/update/<int:id>/', order_update_view, name='order_update'),

    # TASK URLS
    path('tasks/', task_list_view, name='tasks'),
    path('task/<int:id>/', task_detail_view, name='task_detail'),
    path('task/add/<int:order_id>/', task_add_view, name='task_add'),
    path('task/update/<int:id>/', task_update_view, name='task_update'),
    path('task/delete/', task_delete_view, name='task_delete'),
]
