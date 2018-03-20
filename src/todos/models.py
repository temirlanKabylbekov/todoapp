from django.db import models

from app.models import TimestampedModel


class Todo(TimestampedModel):

    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    has_completed = models.BooleanField(default=False)

    assigned = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='assigned_todos', null=True, blank=True)
    todolist = models.ForeignKey('todolists.TodoList', on_delete=models.CASCADE, related_name='todos', null=True)

    def __str__(self):
        return self.title
