# openai_service.py

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-004",  # or the appropriate model
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
