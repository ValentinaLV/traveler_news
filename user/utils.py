from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email(subject, message, email_to):
    email = EmailMessage(
        from_email='traveler@news.com',
        subject=subject,
        to=email_to,
        body=message
    )
    email.send()
