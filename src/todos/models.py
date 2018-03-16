from django.contrib.auth.models import User
from django.db import models

from app.models import DefaultManager, DefaultQueryset, TimestampedModel


class TodoQueryset(DefaultQueryset):

    def created_by_user(self, user):
        return self.filter(author=user)

    def assigned_to_user(self, user):
        return self.filter(assigned=user)

    def available_to_user(self, user):
        return self.created_by_user(user) | self.assigned_to_user(user)


class Todo(TimestampedModel):

    objects = DefaultManager.from_queryset(TodoQueryset)()

    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    has_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_todos')
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_todos', null=True, blank=True)

    def __str__(self):
        return self.title
