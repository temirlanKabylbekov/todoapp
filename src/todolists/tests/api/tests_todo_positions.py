import pytest

from app.test import ApiTestCase, mixer, status

pytestmark = pytest.mark.django_db


def test_user_authentication(api_client):
    response = api_client.put('/api/v1/lists/100500/todo_positions/', {'todos': [3, 2, 1]})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoPositioningInTodoList(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.todolist = mixer.blend('todolists.TodoList', author=cls.user)
        todos = mixer.cycle(3).blend('todos.Todo', todolist=cls.todolist)
        cls.todo_ids = [todo.id for todo in todos]

    def test_passing_incorrect_length_todos(self):
        response = self.c.put('/api/v1/lists/%d/todo_positions/' % self.todolist.id, {'todos': self.todo_ids[:2]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_passing_todo_id_not_belongs_to_todolist(self):
        todo_ids = self.todo_ids[:2] + [100500]
        response = self.c.put('/api/v1/lists/%d/todo_positions/' % self.todolist.id, {'todos': todo_ids})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_todo_positions(self):
        self.api_put('/api/v1/lists/%d/todo_positions/' % self.todolist.id, {'todos': self.todo_ids[::-1]})
        self.todolist.refresh_from_db()
        assert list(self.todolist.todos.values_list('id', flat=True)) == self.todo_ids[::-1]


class TestNamedTodoPositionsInTodoList(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.todolist = mixer.blend('todolists.TodoList', author=cls.user)
        mixer.blend('todos.Todo', todolist=cls.todolist, title='A', is_important=True)
        mixer.blend('todos.Todo', todolist=cls.todolist, title='B', is_important=False)
        mixer.blend('todos.Todo', todolist=cls.todolist, title='C')

    def test_pass_incorrect_name(self):
        response = self.c.put('/api/v1/lists/%d/todo_positions_by_name/' % self.todolist.id, {'name': 'KUKU'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_todo_positions_by_alphabet_asc_order(self):
        self.api_put('/api/v1/lists/%d/todo_positions_by_name/' % self.todolist.id, {'name': 'alphabet'})
        assert list(self.todolist.todos.values_list('title', flat=True)) == ['A', 'B', 'C']

    def test_set_todo_positions_by_alphabet_desc_order(self):
        self.api_put('/api/v1/lists/%d/todo_positions_by_name/' % self.todolist.id, {'name': 'alphabet', 'asc': False})
        assert list(self.todolist.todos.values_list('title', flat=True)) == ['C', 'B', 'A']

    def test_set_todo_positions_by_importance_asc_order(self):
        self.api_put('/api/v1/lists/%d/todo_positions_by_name/' % self.todolist.id, {'name': 'importance'})
        assert list(self.todolist.todos.values_list('title', flat=True)) == ['C', 'B', 'A']

    def test_set_todo_positions_by_importance_desc_order(self):
        self.api_put('/api/v1/lists/%d/todo_positions_by_name/' % self.todolist.id, {'name': 'importance', 'asc': False})
        assert list(self.todolist.todos.values_list('title', flat=True)) == ['A', 'C', 'B']
