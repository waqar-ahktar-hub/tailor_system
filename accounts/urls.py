from django.urls import path
from . import views
from .views import CustomLoginView
app_name = 'accounts'  # Define app namespace
urlpatterns = [
    # path('signup/', views.signup_view, name='signup'),
    # path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.ClientDashboardView.as_view(), name='dashboard'),
     path('activity/', views.activity_view, name='activity'),
]
