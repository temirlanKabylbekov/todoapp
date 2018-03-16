from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient

from .test_case import TestCase

USER_PASSWORD = '123456'


class ApiTestCase(TestCase):

    c = APIClient()
    unauth_c = APIClient()

    should_create_another_user = False
    should_be_logged_in = True

    @classmethod
    def setUpClass(cls):
        if cls.should_create_another_user is True:
            cls.create_another_user()

        if cls.should_be_logged_in is True:
            cls._login()

        super().setUpClass()

    def api_get(self, *args, **kwargs):
        return self._api_call('get', status.HTTP_200_OK, *args, **kwargs)

    def api_post(self, *args, **kwargs):
        return self._api_call('post', status.HTTP_201_CREATED, *args, **kwargs)

    def api_put(self, *args, **kwargs):
        return self._api_call('put', status.HTTP_200_OK, *args, **kwargs)

    def api_delete(self, *args, **kwargs):
        return self._api_call('delete', status.HTTP_204_NO_CONTENT, *args, **kwargs)

    def _api_call(self, method, expected, *args, **kwargs):
        kwargs['format'] = kwargs.get('format', 'json')

        method = getattr(self.c, method)
        response = method(*args, **kwargs)

        content = response.json() if len(response.content) else None

        assert response.status_code == expected, content

        return content

    @classmethod
    def create_user(cls):
        """If you want to create user on your way - just override this method in child test class"""
        user = mixer.blend('auth.User')
        user.set_password(USER_PASSWORD)
        user.save()
        cls.user = user

    @classmethod
    def create_another_user(cls):
        """If you want to create another user on your way - just override this method in child test class"""
        user = mixer.blend('auth.User')
        user.set_password(USER_PASSWORD)
        user.save()
        cls.another_user = user

    @classmethod
    def _login(cls):
        cls.create_user()
        response = cls.c.post('/api/v1/auth/token/', {'username': cls.user.username, 'password': USER_PASSWORD}, format='json')
        cls.c.credentials(HTTP_AUTHORIZATION='JWT %s' % response.json()['token'])
