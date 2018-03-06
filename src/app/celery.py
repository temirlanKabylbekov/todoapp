from __future__ import absolute_import

import locale
import os

from celery import Celery
from django.conf import settings

__all__ = ['celery']

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

celery = Celery('app')

celery.config_from_object(settings)
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
