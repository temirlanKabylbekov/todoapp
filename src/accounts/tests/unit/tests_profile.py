from django.core import mail

from app.test import TestCase, mixer


class TestProfileModel(TestCase):

    def test_sending_email(self):
        user = mixer.blend('auth.User', email='puppy@gmail.com')
        user.profile.send_email('email/test.html', {'username': 'Michael Jordan'})

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ['puppy@gmail.com']
