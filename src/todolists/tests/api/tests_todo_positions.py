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
