from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

# set the default Django settings module for the 'celery' program.
if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

