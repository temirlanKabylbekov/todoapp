from unittest.mock import Mock

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from accounts.models import Profile
from app.test import TestCase


class TestCreatingProfile(TestCase):

    def test_signal_called(self):
        handler = Mock()
        post_save.connect(handler, sender=User)
        User.objects.create(username='monty python')
        assert handler.call_count == 1

    def test_creating_profile(self):
        user = User.objects.create(username='guido van rossum')
        Profile.objects.get(user=user)
