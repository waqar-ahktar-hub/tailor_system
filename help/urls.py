from django.urls import path
from .views import HelpListView, HelpDetailView, HelpSearchView, submit_feedback

app_name = 'help'

urlpatterns = [
    path('', HelpListView.as_view(), name='help_index'),  # Ensure this name matches the one used in your templates
    path('<int:pk>/', HelpDetailView.as_view(), name='help_detail'),
    path('search/', HelpSearchView.as_view(), name='help_search'),
    path('feedback/', submit_feedback, name='help_feedback'),
]
