# # views.py
# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# import openai
# from django.conf import settings

# openai.api_key = settings.OPENAI_API_KEY

# @api_view(['POST'])
# def chat_view(request):
#     user_message = request.data.get('message')
    
#     if not user_message:
#         return JsonResponse({'error': 'Message is required'}, status=400)

#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=user_message,
#         max_tokens=150
#     )

#     ai_response = response.choices[0].text.strip()

#     # Optionally save to database
#     # ChatMessage.objects.create(user_message=user_message, ai_response=ai_response)

#     return JsonResponse({'response': ai_response})
# views.py

from django.http import JsonResponse
from .utils import get_chatgpt_response

def chatgpt_view(request):
    if request.method == 'POST':
        data = request.POST
        prompt = data.get('prompt', '')
        
        if prompt:
            response = get_chatgpt_response(prompt)
            return JsonResponse({'response': response})
        else:
            return JsonResponse({'error': 'No prompt provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.shortcuts import render

def chatgpt_form_view(request):
    return render(request, 'chat.html')