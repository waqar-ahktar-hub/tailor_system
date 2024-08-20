# from django.db import models

# # Create your models here.
# # chat/models.py

# from django.db import models
# from django.contrib.auth.models import User

# class Conversation(models.Model):
#     """Model for a conversation between a client and admin."""
#     client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_conversations')
#     admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_conversations')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Conversation between {self.client.username} and {self.admin.username}"

# class Message(models.Model):
#     """Model for a chat message."""
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)  # Track if the message has been read

#     def __str__(self):
#         return f"Message from {self.sender.username} at {self.created_at}"
# chat/models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.message}"

# from django.db import models
# from django.conf import settings

# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f'{self.sender} -> {self.receiver}: {self.content[:50]}'
