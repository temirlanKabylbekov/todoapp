from django.core import mail
from django.test import override_settings

from app.test import TestCase, mixer


@override_settings(EMAIL_FROM='wunderlist@gmail.com')
class TestProfileModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend('auth.User', email='puppy@gmail.com')
        cls.another_user = mixer.blend('auth.User', first_name='Том', last_name='Харди')
        cls.todolist = mixer.blend('todolists.TodoList', name='Задачи по Маркетингу')

    def test_sending_email(self):
        self.user.profile.send_email('email/test.html', {'username': 'Michael Jordan'})

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ['puppy@gmail.com']

    def test_sending_email_to_invitate_to_todolist(self):
        self.user.profile.send_email_about_invitation_to_todolist(self.another_user, self.todolist)

        email = mail.outbox[0]
        assert email.to == ['puppy@gmail.com']
        assert email.from_email == 'wunderlist@gmail.com'
        assert email.subject == 'Пользователь Том Харди поделился с вами списком'
        assert email.body == 'Пользователь Том Харди поделился с вами списком «Задачи по Маркетингу»'

    def test_sending_email_to_exclude_from_todolist(self):
        self.user.profile.send_email_about_excluding_from_todolist(self.another_user, self.todolist)

        email = mail.outbox[0]
        assert email.to == ['puppy@gmail.com']
        assert email.from_email == 'wunderlist@gmail.com'
        assert email.subject == 'Пользователь Том Харди удалил вас из списка'
        assert email.body == 'Пользователь Том Харди удалил вас из списка «Задачи по Маркетингу»'
