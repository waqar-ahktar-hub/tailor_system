# """urls for tms application."""

# from django.urls import path

# from tailor_management_system.views.apis_view import api_login_view,LogoutView
# from tailor_management_system.views.views import dashboard_view

# app_name = 'tailor_management_system'
# urlpatterns = [
#     path('', dashboard_view, name='dashboard'),

#     # API Token Based Authentication End Points
#     path('api/login', api_login_view, name='login_api'),
#     path('api/logout', LogoutView.as_view(), name='logout_api'),
# ]


# urls.py

from django.urls import path
from tailor_management_system.views.apis_view import api_login_view, LogoutView
from tailor_management_system.views.views import dashboard_view
from client.views.client_views import ClientDashboardView  # Import the new dashboard view

app_name = 'tailor_management_system'
urlpatterns = [
    path('', dashboard_view, name='dashboard'),

    # API Token Based Authentication End Points
    path('api/login', api_login_view, name='login_api'),
    path('api/logout', LogoutView.as_view(), name='logout_api'),

    # Client dashboard view
    path('client/dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
]
