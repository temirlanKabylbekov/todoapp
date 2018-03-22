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

    def update_tags(self):
        current_tags = set(self.tags.values_list('name', flat=True))
        new_tags = self.get_tags_from_title()

        tags_to_remove = current_tags - new_tags
        tags_to_add = new_tags - current_tags

        self.tags.filter(name__in=tags_to_remove).delete()
        Tag.objects.bulk_create([Tag(name=name, todo=self) for name in tags_to_add])

    def get_tags_from_title(self):
        return {tag.strip('#') for tag in self.title.split() if tag.startswith("#") and tag.strip('#')}


class Tag(TimestampedModel):

    name = models.CharField(max_length=255)
    todo = models.ForeignKey('todos.Todo', on_delete=models.CASCADE, related_name='tags', null=True)

    def __str__(self):
        return self.name
