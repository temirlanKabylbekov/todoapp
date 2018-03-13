from django.contrib.auth.models import User
from django.db import models

from app.models import TimestampedModel


class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
