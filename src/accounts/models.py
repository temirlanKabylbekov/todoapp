from django.contrib.auth.models import User
from django.db import models

from app.email import TemplatedEmail
from app.models import TimestampedModel


class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def send_email(self, template_name, context):
        """all users have email - rule when signing up"""
        t = TemplatedEmail(template_name, context, [self.user.email])
        t.send()
