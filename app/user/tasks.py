from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email(user_email, code):
    subject = 'Verify your email'
    message = f'Your verification code is {code}'
    from_email = 'foliocoins@gmail.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
