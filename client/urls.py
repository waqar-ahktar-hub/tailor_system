"""urls for client application."""

from django.urls import path

from client.client_apis import client_detail_view_api, client_view
from client.views.client_views import (
    client_add_view,
    client_delete_view,
    client_detail_view,
    client_list_view,
    client_update_view
)
from client.views.measurement_views import measurements_add_view, measurements_update_view

app_name = 'client'

urlpatterns = [
    path('clients/', client_list_view, name='clients'),
    path('clients/detail/<int:pk>/', client_detail_view, name='client_detail'),
    path('clients/delete/', client_delete_view, name='client_delete'),
    path('clients/add/', client_add_view, name='client_add'),
    path('clients/update/<int:pk>/', client_update_view, name='client_update'),
    path('clients/measurements/add/<int:client_id>/', measurements_add_view, name='measurment_add'),
    path('clients/measurements/update/<int:client_id>/', measurements_update_view, name='measurment_update'),

    # API END POINTS
    path('clients/api/', client_view, name='clients_api'),
    path('clients/api/detail/<int:pk>/', client_detail_view_api, name='client_detail_api'),
    path('clients/api/delete/<int:pk>/', client_detail_view_api, name='client_delete_api'),
    path('clients/api/add/', client_view, name='client_add_api'),
    path('clients/api/update/<int:pk>/', client_detail_view_api, name='client_update_api'),
]
