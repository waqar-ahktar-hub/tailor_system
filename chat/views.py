# chat/views.py

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Message

# @login_required
# def message_dashboard(request):
#     if request.user.is_superuser:
#         # Superuser view
#         messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
#     else:
#         # Client view
#         messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
#     return render(request, 'chat/message_dashboard.html', {'messages': messages})
# # chat/views.py

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def chat_room(request, room_name):
#     return render(request, 'chat/chat_room.html', {
#         'room_name': room_name
#     })
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Message
# from django.contrib.auth.models import User
# from django.utils import timezone

# @login_required
# def chat_room(request, room_name):
#     # Determine the receiver based on room_name (this could be dynamic or a fixed superuser)
#     receiver = User.objects.filter(is_superuser=True).first()
    
#     if request.method == 'POST':
#         content = request.POST.get('message')
#         if content:
#             Message.objects.create(
#                 sender=request.user,
#                 receiver=receiver,
#                 message=content
#             )
#         return redirect('chat_room', room_name=room_name)
    
#     # Get messages for the specific chat room
#     messages = Message.objects.filter(
#         sender=request.user, receiver=receiver
#     ).union(
#         Message.objects.filter(sender=receiver, receiver=request.user)
#     ).order_by('timestamp')
    
#     return render(request, 'chat/chat_room.html', {
#         'room_name': room_name,
#         'messages': messages,
#         'receiver': receiver
#     })

# @login_required
# def superuser_dashboard(request):
#     if not request.user.is_superuser:
#         return HttpResponse("Unauthorized", status=401)
    
#     # Fetch messages and clients based on your logic
#     messages = Message.objects.filter(receiver=request.user)
#     clients = User.objects.exclude(id=request.user.id)  # Assuming you want to exclude the current user

#     # Set a default client_id if needed
#     default_client_id = clients.first().id if clients.exists() else None
    
#     context = {
#         'messages': messages,
#         'clients': clients,
#         'client_id': default_client_id  # Default or selected client_id
#     }
#     return render(request, 'chat/superuser_dashboard.html', context)

# from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse
# import logging

# logger = logging.getLogger(__name__)

# @login_required
# def send_reply(request):
#     if request.method == 'POST':
#         message_content = request.POST.get('message')
#         client_id = request.POST.get('client_id')
        
#         logger.debug(f"Received client_id: {client_id}")
#         logger.debug(f"Received message_content: {message_content}")
        
#         if client_id and message_content:
#             try:
#                 receiver = User.objects.get(id=client_id)
#                 Message.objects.create(
#                     sender=request.user,
#                     receiver=receiver,
#                     message=message_content
#                 )
#                 return redirect('superuser_dashboard')
#             except User.DoesNotExist:
#                 return HttpResponse("User not found", status=404)
#         else:
#             return HttpResponse("Invalid input", status=400)
#     else:
#         return HttpResponse("Invalid request method", status=405)



# new
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def chat_room(request, room_name):
    # Determine the receiver (superuser in this case)
    receiver = User.objects.filter(is_superuser=True).first()
    
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message=content
            )
        return redirect('chat:chat_room', room_name=room_name)
    
    # Get messages for the specific chat room
    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ).union(
        Message.objects.filter(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    # Set a default room name if not provided
    if room_name == 'client-to-superuser':
        room_name = f'{request.user.id}-{receiver.id}'

    return render(request, 'chat/chat_room.html', {
        'room_name': room_name,
        'messages': messages,
        'receiver': receiver
    })
# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
@login_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return JsonResponse({'status': 'success'})

@login_required
def unread_message_count(request):
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q

@login_required
def superuser_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)
    
    # Fetch messages grouped by clients
    clients = User.objects.exclude(id=request.user.id)
    messages_by_client = {}
    unread_messages_count = 0
    
    for client in clients:
        client_messages = Message.objects.filter(
            Q(sender=client, receiver=request.user) |
            Q(sender=request.user, receiver=client)
        ).order_by('-timestamp')
        
        # Count unread messages for the superuser
        unread_messages_count += Message.objects.filter(
            receiver=request.user, sender=client, is_read=False
        ).count()

        messages_by_client[client] = client_messages
    
    # Mark messages as read for the current user
    Message.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    default_client_id = clients.first().id if clients.exists() else None
    
    context = {
        'messages_by_client': messages_by_client,
        'unread_messages_count': unread_messages_count,
        'default_client_id': default_client_id
    }
    return render(request, 'chat/superuser_dashboard.html', context)

@login_required
def send_reply(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        client_id = request.POST.get('client_id')
        
        if client_id and message_content:
            try:
                receiver = User.objects.get(id=client_id)
                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    message=message_content
                )
                return redirect('chat:superuser_dashboard')
            except User.DoesNotExist:
                return HttpResponse("User not found", status=404)
        else:
            return HttpResponse("Invalid input", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)
