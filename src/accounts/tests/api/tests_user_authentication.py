import pytest
from django.contrib.auth.models import User

from accounts.models import Profile
from app.test import mixer, status

pytestmark = pytest.mark.django_db


# TODO: add tests for login, logout and getting authenticated user personal data
class TestUserSignup:

    def test_signup_api_response(self, api_client):
        auth_data = {'username': 'golovkin', 'email': 'ggg@m.kz', 'password1': '123456', 'password2': '123456'}
        response = api_client.post('/api/v1/auth/signup/', auth_data, format='json').data

        assert response['user']['username'] == 'golovkin'
        assert response['user']['email'] == 'ggg@m.kz'

    def test_creating_user(self, api_client):
        auth_data = {'username': 'mayweather', 'email': 'money@m.usa', 'password1': '123456', 'password2': '123456'}
        api_client.post('/api/v1/auth/signup/', auth_data, format='json')

        u = User.objects.get(username='mayweather', email='money@m.usa')
        assert u.check_password('123456') is True

    def test_creating_profile(self, api_client):
        auth_data = {'username': 'joshua', 'email': 'antony@m.uk', 'password1': '123456', 'password2': '123456'}
        api_client.post('/api/v1/auth/signup/', auth_data)
        assert Profile.objects.filter(user=User.objects.get(username='joshua')).exists()

    def test_signing_up_with_existing_user_data(self, api_client):
        mixer.blend('auth.User', username='kanello')

        auth_data = {'username': 'kanello', 'password1': '123456', 'password2': '123456'}
        response = api_client.post('/api/v1/auth/signup/', auth_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['username'] == ['Пользователь с таким именем уже существует.']
