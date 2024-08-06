from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('alert', 'Alert'),
        ('event', 'Event'),
        ('log', 'Log'),
    ]
   
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    target_url = models.URLField(blank=True, null=True)  # Add this field
    
    def __str__(self):
        return self.title
