from app.test import ApiTestCase, mixer, status
from todos.models import Todo


class TestTodoCreating(ApiTestCase):

    should_create_another_user = True

    def test_availability_only_for_authenticated_user(self):
        response = self.unauth_c.post('/api/v1/todos/', {'title': 'Прочитать Мартина Идена'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_setting_user_as_todo_author(self):
        response = self.api_post('/api/v1/todos/', {'title': 'Прочитать Данте Алигьери'})
        todo = Todo.objects.get(id=response['id'])
        assert todo.author == self.user

    def test_creating_todo(self):
        response = self.api_post('/api/v1/todos/', {
            'title': 'Прочитать Эдгара По',
            'due_date': '2018-03-16 11:00',
            'description': 'Прочитать его хоррор-произведение "Лягушонок"',
            'is_important': True,
            'has_completed': False,
            'assigned': self.another_user.id,
        })
        todo = Todo.objects.get(id=response['id'])

        assert todo.author == self.user
        assert todo.assigned == self.another_user
        assert todo.has_completed is False
        assert todo.is_important is True
        assert todo.description == 'Прочитать его хоррор-произведение "Лягушонок"'
        assert todo.due_date == self.datetime(2018, 3, 16, 11, 0)

    def test_api_output(self):
        response = self.api_post('/api/v1/todos/', {
            'title': 'Прочитать Франца Кафка',
            'due_date': '2018-03-16 11:00:00',
            'description': 'Прочитать в оригинале сборник рассказов: "Превращение"',
            'is_important': True,
            'has_completed': False,
            'assigned': self.another_user.id,
        })

        assert response['title'] == 'Прочитать Франца Кафка'
        assert response['due_date'] == '2018-03-16 11:00'
        assert response['description'] == 'Прочитать в оригинале сборник рассказов: "Превращение"'
        assert response['is_important'] is True
        assert response['has_completed'] is False
        assert response['assigned'] == self.another_user.id
        assert response['author'] == self.user.id


class TestTodoUpdating(ApiTestCase):

    should_create_another_user = True

    @classmethod
    def setUpTestData(cls):
        cls.todo1 = mixer.blend('todos.Todo', author=cls.user)
        cls.todo2 = mixer.blend('todos.Todo', author=cls.another_user)

    def test_not_allowed_to_update_strange_user_todo(self):
        response = self.c.put('/api/v1/todos/%d/' % self.todo2.id, {'has_completed': True})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_possible_for_authenticated_user(self):
        response = self.unauth_c.put('/api/v1/todos/%d/' % self.todo1.id, {'is_important': True})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_model(self):
        self.api_put('/api/v1/todos/%d/' % self.todo1.id, {
            'title': 'заголовок',
            'due_date': '2018-03-16 11:00',
            'description': 'описание',
            'is_important': True,
            'has_completed': False,
            'assigned': self.another_user.id,
        })
        self.todo1.refresh_from_db()

        assert self.todo1.title == 'заголовок'
        assert self.todo1.due_date == self.datetime(2018, 3, 16, 11, 0)
        assert self.todo1.description == 'описание'
        assert self.todo1.is_important is True
        assert self.todo1.has_completed is False
        assert self.todo1.assigned == self.another_user

    def test_update_api_output(self):
        response = self.api_put('/api/v1/todos/%d/' % self.todo1.id, {
            'title': 'заголовок',
            'due_date': '2018-03-16 11:00',
            'description': 'описание',
            'is_important': True,
            'has_completed': False,
            'assigned': self.another_user.id,
        })
        assert response['id'] == self.todo1.id
        assert response['title'] == 'заголовок'
        assert response['description'] == 'описание'
        assert response['due_date'] == '2018-03-16 11:00'
        assert response['is_important'] is True
        assert response['has_completed'] is False
        assert response['assigned'] == self.another_user.id


class TestTodoRetrieving(ApiTestCase):

    should_create_another_user = True

    @classmethod
    def setUpTestData(cls):
        cls.todo1 = mixer.blend(
            'todos.Todo', author=cls.user, title='title', description='description',
            due_date=cls.datetime(2015, 1, 1, 11, 30), is_important=True, assigned=cls.another_user,
        )
        cls.todo2 = mixer.blend('todos.Todo', author=cls.another_user)

    def test_not_allowed_to_retrieve_strange_user_todo(self):
        response = self.c.get('/api/v1/todos/%d/' % self.todo2.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_available_only_for_authenticated_user(self):
        response = self.unauth_c.get('/api/v1/todos/%d/' % self.todo1.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # TODO: fix it: cls.datetime, timezone
    # def test_retrieve_output(self):
    #     response = self.api_get('/api/v1/todos/%d/' % self.todo1.id)
    #     assert response['id'] == self.todo1.id
    #     assert response['title'] == 'title'
    #     assert response['due_date'] == '2015-01-01 11:30'
    #     assert response['description'] == 'description'
    #     assert response['is_important'] is True
    #     assert response['has_completed'] is False
    #     assert response['assigned'] == self.another_user


class TestTodoDeleting(ApiTestCase):

    should_create_another_user = True

    @classmethod
    def setUpTestData(cls):
        cls.todo2 = mixer.blend('todos.Todo', author=cls.another_user)

    def test_strange_todo_not_available(self):
        response = self.c.delete('/api/v1/todos/%d/' % self.todo2.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_todo(self):
        todo = mixer.blend('todos.Todo', author=self.user)
        self.api_delete('/api/v1/todos/%d/' % todo.id)
        assert Todo.objects.filter(id=todo.id).first() is None

    def test_user_authentication_for_deleting(self):
        response = self.unauth_c.delete('/api/v1/todos/%d/' % self.todo2.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# TODO: разобраться с проблемами пагинации
# TODO: может стоит should_create_another_user по дефолту поставить в False
class TestTodoListing(ApiTestCase):

    should_create_another_user = True

    @classmethod
    def setUpTestData(cls):
        cls.todo1 = mixer.blend('todos.Todo', author=cls.user)
        cls.todo2 = mixer.blend('todos.Todo', author=mixer.blend('auth.User'), assigned=cls.user)
        cls.todo3 = mixer.blend('todos.Todo', author=cls.another_user)

    def test_created_by_user_todos_are_available(self):
        response = self.api_get('/api/v1/todos/')['results']
        todo_ids = [todo['id'] for todo in response]
        assert self.todo1.id in todo_ids

    def test_assigned_to_user_todos_are_available(self):
        response = self.api_get('/api/v1/todos/')['results']
        todo_ids = [todo['id'] for todo in response]
        assert self.todo2.id in todo_ids

    def test_strange_todos_are_not_available(self):
        response = self.api_get('/api/v1/todos/')['results']
        todo_ids = [todo['id'] for todo in response]
        assert self.todo3.id not in todo_ids

    def test_user_authentication_for_listing(self):
        response = self.unauth_c.get('/api/v1/todos/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
