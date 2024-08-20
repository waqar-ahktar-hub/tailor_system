# # chat/urls.py

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ConversationViewSet, MessageViewSet

# router = DefaultRouter()
# router.register(r'conversations', ConversationViewSet)
# router.register(r'messages', MessageViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
# # chat/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('messages/', views.message_dashboard, name='message_dashboard'),
#     path('<str:room_name>/', views.chat_room, name='chat_room'),
# ]
from django.urls import path
from . import views
app_name = 'chat'
urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('superuser_dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('send-reply/', views.send_reply, name='send_reply'),
     path('mark-message-as-read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'),
    path('unread-message-count/', views.unread_message_count, name='unread_message_count'),

]
