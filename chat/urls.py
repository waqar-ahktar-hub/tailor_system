# urls.py

from django.urls import path
from .views import chatgpt_view,chatgpt_form_view

urlpatterns = [
    path('chat/', chatgpt_form_view, name='chatgpt_form'),
    path('chatgpt/', chatgpt_view, name='chatgpt'),
]
