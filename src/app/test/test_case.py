from datetime import datetime

import pytz
from django.conf import settings
from django.test import TestCase
from django.utils import timezone


class FixtureReaderMixin:

    @classmethod
    def read_fixture(cls, src, binary=False):
        mode = 'r'
        if binary:
            mode = 'rb'
        with open(src, mode) as f:
            return f.read()


class TestCase(FixtureReaderMixin, TestCase):

    @staticmethod
    def datetime(*args, **kwargs):
        """
        Create a timezoned datetime
        """
        if isinstance(args[0], int):
            tz = settings.TIME_ZONE
        else:
            tz = args[0]
            args = args[1:]

        tz = pytz.timezone(tz)
        return timezone.make_aware(
            datetime(*args, **kwargs),
            timezone=tz,
        )
