"""urls for tms application."""

from django.urls import path

from tailor_management_system.views.apis_view import api_login_view
from tailor_management_system.views.views import dashboard_view

app_name = 'tailor_management_system'
urlpatterns = [
    path('', dashboard_view, name='dashboard'),

    # API Token Based Authentication End Points
    path('api/login', api_login_view, name='login_api'),
]
