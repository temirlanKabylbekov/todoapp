from unittest.mock import patch

from django.test import override_settings

from app.test import ApiTestCase, mixer, status


@patch('todolists.tasks.send_email_about_invitation_to_todolist.delay')
@override_settings(
    ENABLE_NOTIFICATIONS=True,
    EMAIL_ENABLED=True,
    CELERY_ALWAYS_EAGER=True,
)
class TestInviteUserToTodoList(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.todolist = mixer.blend('todolists.TodoList', author=cls.user)

    def setUp(self):
        self.inviting_user = mixer.blend('auth.User')

    def test_inviting_user(self, *args):
        self.c.post('/api/v1/lists/%d/invite_user/' % self.todolist.id, {'id': self.inviting_user.id})
        assert self.inviting_user in self.todolist.accessed_users.all()

    def test_try_to_invite_by_not_existing_user_id(self, *args):
        response = self.c.post('/api/v1/lists/%d/invite_user/' % self.todolist.id, {'id': 100500})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_try_to_invite_invited_user(self, *args):
        self.todolist.accessed_users.add(self.inviting_user)
        response = self.c.post('/api/v1/lists/%d/invite_user/' % self.todolist.id, {'id': self.inviting_user.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['user is already invited']

    def test_try_to_invite_user_for_not_found_todolist(self, *args):
        response = self.c.post('/api/v1/lists/100500/invite_user/', {'id': self.inviting_user.id})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_params_passing_to_task_to_send_email(self, invite_task):
        self.c.post('/api/v1/lists/%d/invite_user/' % self.todolist.id, {'id': self.inviting_user.id})
        assert invite_task.call_args == ((self.user.id, self.inviting_user.id, self.todolist.id),)


@patch('todolists.tasks.send_email_about_excludation_from_todolist.delay')
@override_settings(
    ENABLE_NOTIFICATIONS=True,
    EMAIL_ENABLED=True,
    CELERY_ALWAYS_EAGER=True,
)
class TestRemoveUserFromTodoList(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.todolist = mixer.blend('todolists.TodoList', author=cls.user)

    def setUp(self):
        self.invited_user = mixer.blend('auth.User')
        self.todolist.accessed_users.add(self.invited_user)

    def test_excluding_user(self, *args):
        self.c.post('/api/v1/lists/%d/exclude_user/' % self.todolist.id, {'id': self.invited_user.id})
        assert self.invited_user not in self.todolist.accessed_users.all()

    def test_try_to_exclude_by_not_existing_user_id(self, *args):
        response = self.c.post('/api/v1/lists/%d/exclude_user/' % self.todolist.id, {'id': 100500})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_try_to_exclude_not_invited_user(self, *args):
        response = self.c.post('/api/v1/lists/%d/exclude_user/' % self.todolist.id, {'id': mixer.blend('auth.User').id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['user is not invited']

    def test_try_to_exclude_user_for_not_found_todolist(self, *args):
        response = self.c.post('/api/v1/lists/100500/exclude_user/', {'id': self.invited_user.id})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_params_passing_to_task_to_send_email(self, exclude_task):
        self.c.post('/api/v1/lists/%d/exclude_user/' % self.todolist.id, {'id': self.invited_user.id})
        assert exclude_task.call_args == ((self.user.id, self.invited_user.id, self.todolist.id),)
