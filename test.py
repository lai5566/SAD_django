# test_email.py

import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject_vite_api.settings')
django.setup()

send_mail(
    'Test Email',
    'This is a test email.',
    settings.DEFAULT_FROM_EMAIL,
    ['zlai22318@gmail.comm'],
    fail_silently=False,
)
