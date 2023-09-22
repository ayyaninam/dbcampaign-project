import requests
from celery import shared_task
import datetime
from django.core.mail import send_mail


def mail_sender(sender_email, sender_email_password, receiver_emaill):
    send_mail(
        "Email From Ayyan|Django",
        "Here is the message.",
        "ayaaninam555@gmail.com",
        ["carefreekpk@gmail.com"],
        fail_silently=False,
    )


@shared_task
def mail_sender_receiver(sender_email, sender_email_password, receiver_emaill):
    mail_sender(sender_email, sender_email_password, receiver_emaill)
