# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from twilio.rest import Client as TwilioClient
# from .models import Client

# @receiver(post_save, sender=Client)
# def send_welcome_sms(sender, instance, created, **kwargs):
#     if created:
#         # Your Twilio credentials
#         account_sid = settings.TWILIO_ACCOUNT_SID
#         auth_token = settings.TWILIO_AUTH_TOKEN
#         twilio_client = TwilioClient(account_sid, auth_token)

#         message = f"Welcome {instance.name}! Your client account has been created successfully."

#         # Send SMS
#         twilio_client.messages.create(
#             body=message,
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=instance.phone_number
#         )
