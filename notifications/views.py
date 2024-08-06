# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from .models import Notification

# @login_required
# def fetch_notifications(request):
#     notifications = Notification.objects.all()
#     total_count = notifications.count()
#     unread_count = notifications.filter(is_read=False).count()
    
#     notifications_list = list(notifications.values('id', 'title', 'timestamp', 'is_read'))
    
#     return JsonResponse({
#         'notifications': notifications_list,
#         'unread_count': unread_count,
#         'total_count': total_count  # Add this to verify total count
#     })


# @require_POST
# @login_required
# def mark_as_checked(request, id):
#     notification = get_object_or_404(Notification, id=id)
#     notification.is_read = True
#     notification.save()
#     return JsonResponse({'status': 'success'})
# notifications/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def fetch_notifications(request):
    notifications = Notification.objects.all()
    notifications_list = list(notifications.values('id', 'title', 'timestamp', 'is_read', 'target_url'))
    return JsonResponse({'notifications': notifications_list})

@require_POST
@login_required
def mark_as_checked(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.is_read = True
    notification.save()
    
    # Return the count of unread notifications
    unread_count = Notification.objects.filter(is_read=False).count()
    return JsonResponse({'status': 'success', 'unread_count': unread_count})
