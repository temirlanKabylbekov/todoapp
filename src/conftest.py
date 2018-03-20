import pytest
from rest_framework.test import APIClient

from app.test import mixer


@pytest.fixture(scope='class')
def users(request):
    request.cls.user = mixer.blend('auth.User')
    request.cls.another_user = mixer.blend('auth.User')


@pytest.fixture
def api_client(db):
    return APIClient()
