import random
import string
import uuid

from django.core.mail import send_mail

from core import settings


def gen_token():
    return uuid.uuid4().hex[:6].upper()


def gen_password():
    ch = string.ascii_letters + string.digits
    return ''.join(random.choice(ch) for i in range(10))


def send_text(to, subject, message):
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [to])
