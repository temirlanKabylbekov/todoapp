from unittest.mock import patch

from django.test import override_settings

from app.test import TestCase, mixer
from todolists import tasks


@override_settings(
    ENABLE_NOTIFICATIONS=True,
    EMAIL_ENABLED=True,
    CELERY_ALWAYS_EAGER=True,
)
class TestSendingEmailAboutInvitationAndExcludingFromTodolist(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.caller = mixer.blend('auth.User')
        cls.callee = mixer.blend('auth.User')
        cls.todolist = mixer.blend('todolists.TodoList')

    @patch('accounts.models.Profile.send_email_about_invitation_to_todolist')
    def test_sending_invitation(self, send_invite):
        tasks.send_email_about_invitation_to_todolist(self.caller.id, self.callee.id, self.todolist.id)

        assert send_invite.call_count == 1
        assert send_invite.call_args[0] == (self.caller, self.todolist)

    @patch('accounts.models.Profile.send_email_about_excluding_from_todolist')
    def test_sending_excludation(self, send_exclude):
        tasks.send_email_about_excludation_from_todolist(self.caller.id, self.callee.id, self.todolist.id)

        assert send_exclude.call_count == 1
        assert send_exclude.call_args[0] == (self.caller, self.todolist)
