from django.urls import path
from .views import fetch_notifications, mark_as_checked

urlpatterns = [
    path('fetch_notifications/', fetch_notifications, name='fetch_notifications'),
    path('mark_as_checked/<int:id>/', mark_as_checked, name='mark_as_checked'),
]
