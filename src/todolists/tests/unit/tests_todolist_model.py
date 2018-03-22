from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.test import override_settings

from app.test import TestCase, mixer
from todolists.models import TodoList


@pytest.mark.usefixtures('users')
class TestTodoListQueryset(TestCase):

    def test_created_by_user(self):
        todolist = mixer.blend('todolists.TodoList', author=self.user)
        assert todolist in TodoList.objects.created_by_user(self.user)

    def test_created_by_user_not_contains_strange_todolist(self):
        todolist = mixer.blend('todolists.TodoList', author=self.another_user)
        assert todolist not in TodoList.objects.created_by_user(self.user)

    def test_accessed_to_user(self):
        todolist = mixer.blend('todolists.TodoList', author=self.user)
        todolist.accessed_users.add(self.another_user)
        assert todolist in TodoList.objects.accessed_to_user(self.another_user)

    def test_available_to_user_contains_author_todolists(self):
        todolist = mixer.blend('todolists.TodoList', author=self.user)
        assert todolist in TodoList.objects.available_to_user(self.user)

    def test_available_to_user_contains_accessed_users_todolists(self):
        todolist = mixer.blend('todolists.TodoList', author=self.user)
        todolist.accessed_users.add(self.another_user)
        assert todolist in TodoList.objects.available_to_user(self.another_user)


@patch('todolists.tasks.send_email_about_excludation_from_todolist.delay')
@patch('todolists.tasks.send_email_about_invitation_to_todolist.delay')
@override_settings(
    ENABLE_NOTIFICATIONS=True,
    EMAIL_ENABLED=True,
    CELERY_ALWAYS_EAGER=True,
)
class TestInviteAndExcludeUserTodoListMethods(TestCase):

    def setUp(self):
        self.invited_user = mixer.blend('auth.User')
        self.ringleader = mixer.blend('auth.User')
        self.todolist = mixer.blend('todolists.TodoList', accessed_users=self.invited_user)

    def test_invite_user(self, *args):
        user = mixer.blend('auth.User')
        self.todolist.invite_user(self.ringleader, user)
        assert user in self.todolist.accessed_users.all()

    def test_reinviting_the_same_user_raises_error(self, *args):
        with pytest.raises(ValidationError, message='user is already invited'):
            self.todolist.invite_user(self.ringleader, self.invited_user)

    def test_exclude_user(self, *args):
        self.todolist.exclude_user(self.ringleader, self.invited_user)
        assert self.invited_user not in self.todolist.accessed_users.all()

    def test_excluding_user_that_was_not_invited_raises_error(self, *args):
        with pytest.raises(ValidationError, message='user is not invited'):
            self.todolist.exclude_user(self.ringleader, mixer.blend('auth.User'))

    def test_sending_invite_email_task_called(self, invite_task, exclude_task):
        user = mixer.blend('auth.User')
        self.todolist.invite_user(self.ringleader, user)
        assert invite_task.called is True

    def test_sending_exclude_email_task_called(self, invite_task, exclude_task):
        self.todolist.exclude_user(self.ringleader, self.invited_user)
        assert exclude_task.called is True
