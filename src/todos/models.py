from django.db import models

from app.models import DefaultManager, DefaultQueryset, TimestampedModel


class TodoQueryset(DefaultQueryset):

    def created_by_user(self, user):
        return self.filter(todolist__author=user)

    def assigned_to_user(self, user):
        return self.filter(assigned=user)

    def accessed_to_user(self, user):
        return self.filter(todolist__accessed_users=user)

    def available_to_user(self, user):
        available_to_user = self.created_by_user(user) | self.assigned_to_user(user) | self.accessed_to_user(user)
        return available_to_user.distinct()

    def for_viewset(self, user):
        return self.available_to_user(user).order_by('id')


class Todo(TimestampedModel):

    objects = DefaultManager.from_queryset(TodoQueryset)()

    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    has_completed = models.BooleanField(default=False)

    assigned = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='assigned_todos', null=True, blank=True)
    todolist = models.ForeignKey('todolists.TodoList', on_delete=models.CASCADE, related_name='todos', null=True)

    def __str__(self):
        return self.title
