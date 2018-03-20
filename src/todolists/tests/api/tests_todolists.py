import pytest

from app.test import ApiTestCase, mixer, status
from todolists.models import TodoList


@pytest.mark.parametrize('method_name, url, payload', [
    ('get', '/api/v1/lists/', ''),
    ('get', '/api/v1/lists/1/', ''),
    ('delete', '/api/v1/lists/1/', ''),
    ('post', '/api/v1/lists/', {'name': 'Входящее'}),
    ('put', '/api/v1/lists/1/', {'name': 'Спринт'}),
])
def test_user_authentication(api_client, method_name, url, payload):
    args = (url,) if payload == '' else (url, payload)
    response = getattr(api_client, method_name)(*args)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTodoListCreating(ApiTestCase):

    def test_setting_user_as_author_of_todolist(self):
        response = self.api_post('/api/v1/lists/', {'name': 'Входящее'})
        assert TodoList.objects.get(id=response['id']).author == self.user

    def test_creating_todolist(self):
        response = self.api_post('/api/v1/lists/', {'name': 'Входящее'})
        assert TodoList.objects.get(id=response['id']).name == 'Входящее'


@pytest.mark.usefixtures('todolists')
class TestTodoListListing(ApiTestCase):

    def _get_todolist_by_id_in_response(self, todolists, todolist_id):
        for todolist in todolists:
            if todolist['id'] == todolist_id:
                return todolist

    def test_not_contains_strange_todolist(self):
        response = self.api_get('/api/v1/lists/')['results']
        todolist_ids = [todolist['id'] for todolist in response]
        assert self.strange_todolist.id not in todolist_ids

    def test_contains_created_by_user_todolist(self):
        response = self.api_get('/api/v1/lists/')['results']
        todolist_ids = [todolist['id'] for todolist in response]
        assert self.created_todolist.id in todolist_ids

    def test_contains_accessed_to_user_todolist(self):
        response = self.api_get('/api/v1/lists/')['results']
        todolist_ids = [todolist['id'] for todolist in response]
        assert self.accessed_todolist.id in todolist_ids

    def test_getting_todos_of_todolist(self):
        mixer.blend('todos.Todo', todolist=self.created_todolist, title='Позвонить Цукербергу')
        response = self.api_get('/api/v1/lists/')['results']
        todolist = self._get_todolist_by_id_in_response(response, self.created_todolist.id)
        assert todolist['todos'][0]['title'] == 'Позвонить Цукербергу'

    def test_getting_accessed_users_to_todolist(self):
        self.created_todolist.accessed_users.add(self.another_user)
        response = self.api_get('/api/v1/lists/')['results']
        todolist = self._get_todolist_by_id_in_response(response, self.created_todolist.id)
        assert self.another_user.id in todolist['accessed_users']


@pytest.mark.usefixtures('todolists')
class TestTodoListRetrieving(ApiTestCase):

    def test_not_allowed_to_get_strange_todolist(self):
        response = self.c.get('/api/v1/lists/%d/' % self.strange_todolist.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_created_todolist(self):
        response = self.api_get('/api/v1/lists/%d/' % self.created_todolist.id)
        assert response['id'] == self.created_todolist.id

    def test_retrieve_accessed_todolist(self):
        response = self.api_get('/api/v1/lists/%d/' % self.accessed_todolist.id)
        assert response['id'] == self.accessed_todolist.id

    def test_getting_todos_of_todolist(self):
        mixer.blend('todos.Todo', todolist=self.created_todolist, title='Позвонить Цукербергу')
        response = self.api_get('/api/v1/lists/%d/' % self.created_todolist.id)
        assert response['todos'][0]['title'] == 'Позвонить Цукербергу'

    def test_getting_accessed_users_to_todolist(self):
        self.created_todolist.accessed_users.add(self.another_user)
        response = self.api_get('/api/v1/lists/%d/' % self.created_todolist.id)
        assert self.another_user.id in response['accessed_users']


class TestTodoListDeleting(ApiTestCase):

    def test_not_allowed_to_delete_strange_todolist(self):
        strange_todolist = mixer.blend('todolists.TodoList', author=self.another_user)
        response = self.c.delete('/api/v1/lists/%d/' % strange_todolist.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_created_todolist(self):
        created_todolist_id = mixer.blend('todolists.TodoList', author=self.user).id
        self.api_delete('/api/v1/lists/%d/' % created_todolist_id)
        assert TodoList.objects.filter(id=created_todolist_id).first() is None

    def test_delete_accessed_todolist(self):
        accessed_todolist_id = mixer.blend('todolists.TodoList', author=self.another_user, accessed_users=self.user).id
        self.api_delete('/api/v1/lists/%d/' % accessed_todolist_id)
        assert TodoList.objects.filter(id=accessed_todolist_id).first() is None


@pytest.mark.usefixtures('todolists')
class TestTodoListUpdating(ApiTestCase):

    def test_not_allowed_to_update_strange_todolist(self):
        response = self.c.put('/api/v1/lists/%d/' % self.strange_todolist.id, {'name': 'Новое Название'})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_updating_todolist(self):
        self.api_put('/api/v1/lists/%d/' % self.created_todolist.id, {'name': 'Новое Название'})
        self.created_todolist.refresh_from_db()
        assert self.created_todolist.name == 'Новое Название'
