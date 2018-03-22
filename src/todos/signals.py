from django.db.models.signals import post_save
from django.dispatch import receiver

from todos.models import Todo


@receiver(post_save, sender=Todo)
def update_todo_tags(sender, instance, **kwargs):
    # if neccessary, you can call this method asynchronously in celery task
    instance.update_tags()
