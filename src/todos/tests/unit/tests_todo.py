from app.test import TestCase, mixer
from todos.models import Todo


class TestCreatedByUserQueryset(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend('auth.User')

        cls.todo1 = mixer.blend('todos.Todo', author=cls.user)
        cls.todo2 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'))

    def test_return_only_contains_todos_of_given_user(self):
        assert self.todo1 in Todo.objects.created_by_user(self.user)
        assert self.todo2 not in Todo.objects.created_by_user(self.user)


class TestAssignedToUserQueryset(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend('auth.User')

        cls.todo1 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'), assigned=cls.user)
        cls.todo2 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'))
        cls.todo3 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'), assigned=mixer.blend('auth.User'))

    def test_return_only_contains_todos_assigned_to_given_user(self):
        assert self.todo1 in Todo.objects.assigned_to_user(self.user)
        assert self.todo3 not in Todo.objects.assigned_to_user(self.user)

    def test_return_not_contains_todos_with_empty_assigned_user_field(self):
        assert self.todo2 not in Todo.objects.assigned_to_user(self.user)


class TestAvailableToUserQueryset(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend('auth.User')

        cls.todo1 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'), assigned=cls.user)
        cls.todo2 = mixer.blend('todos.Todo', author=cls.user)

    def test_contains_todo_created_by_user(self):
        assert self.todo2 in Todo.objects.available_to_user(self.user)

    def test_contains_todo_assigned_to_User(self):
        assert self.todo1 in Todo.objects.available_to_user(self.user)
