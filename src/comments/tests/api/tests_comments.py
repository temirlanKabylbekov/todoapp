import pytest

from app.test import ApiTestCase, mixer, status
from comments.models import Comment


@pytest.mark.parametrize('method_name, url, payload', [
    ('get', '/api/v1/comments/', ''),
    ('get', '/api/v1/comments/1/', ''),
    ('delete', '/api/v1/comments/1/', ''),
    ('post', '/api/v1/comments/', {'name': 'Входящее'}),
    ('put', '/api/v1/comments/1/', {'name': 'Спринт'}),
])
def test_user_authentication(api_client, method_name, url, payload):
    args = (url,) if payload == '' else (url, payload)
    response = getattr(api_client, method_name)(*args)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures('todolists', 'todos')
class TestCommentCreating(ApiTestCase):

    def test_not_allowed_to_post_comment_in_strange_todo(self):
        response = self.c.post('/api/v1/comments/', {'todo': self.strange_todo.id, 'text': 'Я хочу оставить комментарии'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_comment_in_created_todo(self):
        response = self.api_post('/api/v1/comments/', {'todo': self.created_todo.id, 'text': 'Я хочу оставить комментарии'})
        assert Comment.objects.get(id=response['id']).todo == self.created_todo

    def test_post_comment_in_assigned_todo(self):
        response = self.api_post('/api/v1/comments/', {'todo': self.assigned_todo.id, 'text': 'Я хочу оставить комментарии'})
        assert Comment.objects.get(id=response['id']).todo == self.assigned_todo

    def test_post_comment_in_accessed_todo(self):
        response = self.api_post('/api/v1/comments/', {'todo': self.accessed_todo.id, 'text': 'Я хочу оставить комментарии'})
        assert Comment.objects.get(id=response['id']).todo == self.accessed_todo

    def test_setting_auth_user_as_author_of_comment(self):
        response = self.api_post('/api/v1/comments/', {'todo': self.created_todo.id, 'text': 'Я хочу оставить комментарии'})
        assert Comment.objects.get(id=response['id']).author == self.user


@pytest.mark.usefixtures('todolists', 'todos')
class TestCommentDeleting(ApiTestCase):

    def test_cant_delete_strange_but_available_to_see_comment(self):
        strange_created_todo_comment = mixer.blend('comments.Comment', todo=self.created_todo, author=self.another_user)
        response = self.c.delete('/api/v1/comments/%d/' % strange_created_todo_comment.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cant_delete_strange_and_not_available_comment(self):
        strange_comment = mixer.blend('comments.Comment', todo=self.strange_todo, author=self.another_user)
        response = self.c.delete('/api/v1/comments/%d/' % strange_comment.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_own_comment(self):
        created_todo_comment = mixer.blend('comments.Comment', todo=self.created_todo, author=self.user)
        self.api_delete('/api/v1/comments/%d/' % created_todo_comment.id)
        assert Comment.objects.filter(id=created_todo_comment.id).exists() is False


@pytest.mark.usefixtures('todolists', 'todos')
class TestCommentUpdating(ApiTestCase):

    def test_cant_update_strange_but_available_to_see_comment(self):
        strange_created_todo_comment = mixer.blend('comments.Comment', todo=self.created_todo, author=self.another_user)
        response = self.c.put('/api/v1/comments/%d/' % strange_created_todo_comment.id, {'text': 'новый текст'})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cant_update_strange_and_not_available_comment(self):
        strange_comment = mixer.blend('comments.Comment', todo=self.strange_todo, author=self.another_user)
        response = self.c.put('/api/v1/comments/%d/' % strange_comment.id, {'text': 'новый текст'})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_own_comment(self):
        created_todo_comment = mixer.blend('comments.Comment', todo=self.created_todo, author=self.user)
        response = self.api_put('/api/v1/comments/%d/' % created_todo_comment.id, {'text': 'новый текст'})
        assert Comment.objects.get(id=response['id']).text == 'новый текст'
