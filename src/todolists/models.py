from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from app.models import DefaultManager, DefaultModel, DefaultQueryset


class TodoListQueryset(DefaultQueryset):

    def created_by_user(self, user):
        return self.filter(author=user)

    def accessed_to_user(self, user):
        return self.filter(accessed_users__in=[user])

    def available_to_user(self, user):
        return self.created_by_user(user) | self.accessed_to_user(user)

    def for_viewset(self, user):
        return self.available_to_user(user).prefetch_related('todos').order_by('id')


class TodoList(DefaultModel):

    objects = DefaultManager.from_queryset(TodoListQueryset)()

    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='todolists', null=True)

    accessed_users = models.ManyToManyField('auth.User', related_name='invited_todolists', blank=True)

    def __str__(self):
        return self.name

    def invite_user(self, user):
        if self.accessed_users.filter(id=user.id).exists():
            raise ValidationError('user is already invited')

        self.accessed_users.add(user)

    def exclude_user(self, user):
        if not self.accessed_users.filter(id=user.id).exists():
            raise ValidationError('user is not invited')

        self.accessed_users.remove(user)
