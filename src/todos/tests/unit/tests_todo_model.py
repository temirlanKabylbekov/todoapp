import pytest

from app.test import TestCase
from todos.models import Todo


@pytest.mark.usefixtures('users', 'todolists', 'todos')
class TestTodoQueryset(TestCase):

    def test_created_by_user(self):
        assert self.created_todo in Todo.objects.created_by_user(self.user)

    def test_created_by_user_not_contains_strange_todo(self):
        assert self.strange_todo not in Todo.objects.created_by_user(self.user)

    def test_assigned_to_user(self):
        assert self.assigned_todo in Todo.objects.assigned_to_user(self.user)

    def test_accessed_to_user(self):
        assert self.accessed_todo in Todo.objects.accessed_to_user(self.user)

    def test_available_to_user_contains_created_by_user(self):
        assert self.created_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_assigned_to_user(self):
        assert self.assigned_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_accessed_to_user(self):
        assert self.accessed_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_distinct_todos(self):
        assert Todo.objects.available_to_user(self.user).count() == 3
