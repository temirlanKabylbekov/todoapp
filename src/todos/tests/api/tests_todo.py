import pytest

from app.test import ApiTestCase, status
from todos.models import Todo


@pytest.mark.parametrize('method_name, url, payload', [
    ('get', '/api/v1/todos/', ''),
    ('get', '/api/v1/todos/1/', ''),
    ('delete', '/api/v1/todos/1/', ''),
    ('post', '/api/v1/todos/', {'title': 'Купить билет на ЧМ-2018'}),
    ('put', '/api/v1/todos/1/', {'is_important': True}),
])
def test_user_authentication(api_client, method_name, url, payload):
    args = (url,) if payload == '' else (url, payload)
    response = getattr(api_client, method_name)(*args)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoCreating(ApiTestCase):

    def test_method_not_allowed(self):
        response = self.c.post('/api/v1/todos/', {'title': 'Купить билет на ЧМ-2018'})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data['detail'] == 'use post: `/api/v1/lists/{pk}/` to create todo'


@pytest.mark.usefixtures('todolists', 'todos')
class TestTodoRetrieving(ApiTestCase):

    def test_strange_todo_is_not_available(self):
        response = self.c.get('/api/v1/todos/%d/' % self.strange_todo.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_created_todo_is_available(self):
        response = self.api_get('/api/v1/todos/%d/' % self.created_todo.id)
        assert Todo.objects.get(id=response['id']) == self.created_todo

    def test_assigned_todo_is_available(self):
        response = self.api_get('/api/v1/todos/%d/' % self.assigned_todo.id)
        assert Todo.objects.get(id=response['id']) == self.assigned_todo

    def test_accessed_todo_is_available(self):
        response = self.api_get('/api/v1/todos/%d/' % self.accessed_todo.id)
        assert Todo.objects.get(id=response['id']) == self.accessed_todo


@pytest.mark.usefixtures('todolists', 'todos')
class TestTodoUpdating(ApiTestCase):

    def test_strange_todo_is_not_available(self):
        response = self.c.put('/api/v1/todos/%d/' % self.strange_todo.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_updating_created_todo(self):
        response = self.api_put('/api/v1/todos/%d/' % self.created_todo.id, {'has_completed': True})
        assert Todo.objects.get(id=response['id']).has_completed is True

    def test_updating_assigned_todo(self):
        response = self.api_put('/api/v1/todos/%d/' % self.assigned_todo.id, {'is_important': True})
        assert Todo.objects.get(id=response['id']).is_important is True

    def test_updating_accessed_todo(self):
        response = self.api_put('/api/v1/todos/%d/' % self.accessed_todo.id, {'description': 'описание задачи'})
        assert Todo.objects.get(id=response['id']).description == 'описание задачи'


@pytest.mark.usefixtures('todolists', 'todos')
class TestTodoDeleting(ApiTestCase):

    def test_strange_todo_is_not_available(self):
        response = self.c.delete('/api/v1/todos/%d/' % self.strange_todo.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deleting_created_todo(self):
        self.api_delete('/api/v1/todos/%d/' % self.created_todo.id)
        assert not Todo.objects.filter(id=self.created_todo.id).exists()

    def test_deleting_assigned_todo(self):
        self.api_delete('/api/v1/todos/%d/' % self.assigned_todo.id)
        assert not Todo.objects.filter(id=self.assigned_todo.id).exists()

    def test_deleting_accessed_todo(self):
        self.api_delete('/api/v1/todos/%d/' % self.accessed_todo.id)
        assert not Todo.objects.filter(id=self.accessed_todo.id).exists()
