from behaviors.behaviors import Timestamped
from django.db import models


class DefaultQueryset(models.QuerySet):
    pass


class DefaultManager(models.Manager):
    pass


class DefaultModel(models.Model):
    objects = DefaultManager()

    class Meta:
        abstract = True


class TimestampedModel(DefaultModel, Timestamped):
    """
    Model mixin to add `created` and `modified` attributes to your models
    Based on https://github.com/audiolion/django-behaviors
    """
    class Meta:
        abstract = True
