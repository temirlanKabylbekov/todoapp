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


@pytest.fixture(scope='class')
def todolists(request):
    user = request.cls.user
    another_user = request.cls.another_user

    request.cls.strange_todolist = mixer.blend('todolists.TodoList', author=another_user)
    request.cls.created_todolist = mixer.blend('todolists.TodoList', author=user)
    request.cls.accessed_todolist = mixer.blend('todolists.TodoList', author=another_user, accessed_users=user)


@pytest.fixture(scope='class')
def todos(todolists, request):
    user = request.cls.user

    created_todolist = request.cls.created_todolist
    strange_todolist = request.cls.strange_todolist
    accessed_todolist = request.cls.accessed_todolist

    request.cls.created_todo = mixer.blend('todos.Todo', todolist=created_todolist)
    request.cls.assigned_todo = mixer.blend('todos.Todo', todolist=strange_todolist, assigned=user)
    request.cls.accessed_todo = mixer.blend('todos.Todo', todolist=accessed_todolist)
    request.cls.strange_todo = mixer.blend('todos.Todo', todolist=strange_todolist)
