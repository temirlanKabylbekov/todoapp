import pytest
from django.core import mail
from django.test import override_settings

from app.email import TemplatedEmail


@pytest.fixture(scope='module')
def email():
    return TemplatedEmail('email/test.html', {'username': 'Ален'}, ['receiver@gmail.com'])


@override_settings(EMAIL_ENABLED=False)
def test_not_sending_email_if_email_is_disabled_in_settings(email):
    email.send()
    assert len(mail.outbox) == 0


@override_settings(EMAIL_ENABLED=True, ENABLE_NOTIFICATIONS=False)
def test_not_sending_email_if_notifications_are_disabled_in_settings(email):
    email.send()
    assert len(mail.outbox) == 0


@override_settings(EMAIL_ENABLED=True, ENABLE_NOTIFICATIONS=True)
def test_send_email_if_email_and_notifications_are_enabled_in_settings(email):
    email.send()
    assert len(mail.outbox) == 1


@override_settings(EMAIL_FROM='tester@gmail.com')
def test_setting_default_from_email():
    email = TemplatedEmail('email/test.html', {'username': 'Ален'}, ['receiver@gmail.com'])
    email.send()
    assert mail.outbox[0].from_email == 'tester@gmail.com'


@override_settings(EMAIL_ENABLED=True, ENABLE_NOTIFICATIONS=True)
def test_sending_email_content(email):
    email.send()
    sent_email = mail.outbox[0]

    assert sent_email.subject == 'Ален, добро пожаловать на наш сервис!'
    assert sent_email.to == ['receiver@gmail.com']
    assert 'Ален,' in sent_email.body
