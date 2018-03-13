from django.contrib.auth.models import User

from accounts.models import Profile
from app.test import ApiTestCase, status


class TestUserSignup(ApiTestCase):

    should_be_logged_in = False

    def test_signup_api_response(self):
        auth_data = {'username': 'golovkin', 'email': 'ggg@m.kz', 'password1': '123456', 'password2': '123456'}
        response = self.api_post('/api/v1/auth/signup/', auth_data)

        assert response['user']['username'] == 'golovkin'
        assert response['user']['email'] == 'ggg@m.kz'

    def test_creating_user(self):
        auth_data = {'username': 'mayweather', 'email': 'money@m.usa', 'password1': '123456', 'password2': '123456'}
        self.api_post('/api/v1/auth/signup/', auth_data)

        u = User.objects.get(username='mayweather', email='money@m.usa')
        assert u.check_password('123456') is True

    def test_creating_profile(self):
        auth_data = {'username': 'joshua', 'email': 'antony@m.uk', 'password1': '123456', 'password2': '123456'}
        self.api_post('/api/v1/auth/signup/', auth_data)
        Profile.objects.get(user=User.objects.get(username='joshua'))

    def test_signing_up_with_existing_user_data(self):
        User.objects.create(username='kanello')

        auth_data = {'username': 'kanello', 'password1': '123456', 'password2': '123456'}
        response = self.c.post('/api/v1/auth/signup/', auth_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['username'] == ['Пользователь с таким именем уже существует.']
