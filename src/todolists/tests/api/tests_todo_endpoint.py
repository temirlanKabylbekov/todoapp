import pytest

from app.test import ApiTestCase, mixer, status
from todos.models import Todo

pytestmark = pytest.mark.django_db


def test_user_authentication(api_client):
    response = api_client.post('/api/v1/lists/100500/todos/', {'title': 'Заказать пиццу'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoCreatingInTodoList(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.todolist = mixer.blend('todolists.TodoList', author=cls.user)

    def test_creating_todo(self):
        response = self.api_post('/api/v1/lists/%d/todos/' % self.todolist.id, {'title': 'Заказать пиццу'})
        assert Todo.objects.filter(id=response['id'], title='Заказать пиццу').exists()

    def test_setting_todolist(self):
        response = self.api_post('/api/v1/lists/%d/todos/' % self.todolist.id, {'title': 'Купить кейс колы'})
        assert Todo.objects.get(id=response['id']).todolist == self.todolist

    def test_try_to_create_todo_for_not_found_todolist(self):
        response = self.c.post('/api/v1/lists/100500/todos/', {'title': 'Заказать пиццу'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
