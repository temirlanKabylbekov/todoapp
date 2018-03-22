import pytest

from app.test import TestCase, mixer
from todos.models import Todo

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('users', 'todolists', 'todos')
class TestTodoQueryset(TestCase):

    def test_created_by_user(self):
        assert self.created_todo in Todo.objects.created_by_user(self.user)

    def test_created_by_user_not_contains_strange_todo(self):
        assert self.strange_todo not in Todo.objects.created_by_user(self.user)

    def test_assigned_to_user(self):
        assert self.assigned_todo in Todo.objects.assigned_to_user(self.user)

    def test_accessed_to_user(self):
        assert self.accessed_todo in Todo.objects.accessed_to_user(self.user)

    def test_available_to_user_contains_created_by_user(self):
        assert self.created_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_assigned_to_user(self):
        assert self.assigned_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_accessed_to_user(self):
        assert self.accessed_todo in Todo.objects.available_to_user(self.user)

    def test_available_to_user_contains_distinct_todos(self):
        assert Todo.objects.available_to_user(self.user).count() == 3


@pytest.mark.parametrize('title, expected_tags', [
    ('#продукты Сходить в перекресток', ['продукты']),
    ('# продукты Сходить в перекресток', []),
    ('#продукты#расходы Сходить в перекресток', ['продукты#расходы']),
    ('#продукты #расходы Сходить в перекресток', ['продукты', 'расходы']),
    ('#продукты #расходы', ['продукты', 'расходы']),
    ('Сходить в перекресток #продукты', ['продукты']),
    ('Сходить в перекресток # продукты', []),
    ('Сходить в перекресток #продукты#расходы', ['продукты#расходы']),
    ('Сходить в перекресток #продукты #расходы', ['продукты', 'расходы']),
    ('Сходить в перекресток#продукты', []),
    ('#', []),
    ('Сходить #продукты в #расходы перекресток', ['продукты', 'расходы']),
    ('#продукты #продукты', ['продукты']),
])
def test_get_tags_from_title_method(title, expected_tags):
    todo = mixer.blend('todos.Todo', title=title)
    assert todo.get_tags_from_title() == set(expected_tags)


@pytest.mark.parametrize('old_title, new_title, tags', [
    (
        '#парагвай #путешествия Съездить в Парагвай',
        'Съездить в Уругвай #путешествия #уругвай',
        {'путешествия', 'уругвай'},
    ),
    (
        'Съездить в Гвадалахару',
        'Съездить в Гвадалахару #мексика',
        {'мексика'},
    ),
    (
        'Съездить в Бразилию #бразилия',
        'Съездить в Бразилию',
        set(),
    )
])
def test_update_tags_when_updating_todo_model(old_title, new_title, tags):
    # testing with calling post_save signal: todos.signals.update_todo_tags
    todo = mixer.blend('todos.Todo', title=old_title)
    todo.title = new_title
    todo.save()
    assert set(todo.tags.all().values_list('name', flat=True)) == tags


@pytest.mark.parametrize('title, tags', [
    ('#парагвай #путешествия Съездить в Парагвай', {'путешествия', 'парагвай'}),
    ('Съездить в Гвадалахару', set()),
    ('Съездить в Бразилию #бразилия', {'бразилия'}),
])
def test_update_tags_when_creating_todo_model(title, tags):
    # testing with calling post_save signal: todos.signals.update_todo_tags
    todo = mixer.blend('todos.Todo', title=title)
    assert set(todo.tags.all().values_list('name', flat=True)) == tags
