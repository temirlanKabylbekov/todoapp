import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.test import USER_PASSWORD, mixer
from todos.models import Todo

MY_USER_NAME = 'Jackie'  # use this user to login and test apis


class Command(BaseCommand):

    help = 'Generate random todos, todolists, comments and users'

    def _generate_users(self, count=4):
        mixer.cycle(count).blend('auth.User')
        mixer.blend('auth.User', username=MY_USER_NAME)

        for user in User.objects.iterator():
            user.set_password(USER_PASSWORD)
            user.save()

    def _generate_todolists(self, count=25, max_accessed_users_count=2):
        lists = mixer.cycle(count).blend('todolists.TodoList', author=mixer.SELECT)

        for todolist in lists:
            potential_users = User.objects.exclude(id=todolist.author.id)
            random_users = random.sample(list(potential_users), random.randrange(max_accessed_users_count + 1))
            todolist.accessed_users.set(random_users)
            todolist.save()

    def _generate_todos(self, count=125):
        mixer.cycle(count).blend('todos.Todo', todolist=mixer.SELECT, assigned=mixer.SELECT)

    def _generate_comments(self, count=20):
        comments = mixer.cycle(count).blend('comments.Comment', todo=None, author=mixer.SELECT)
        for comment in comments:
            comment.todo = Todo.objects.available_to_user(comment.author).order_by('?').first()
            comment.save()

    def handle(self, *args, **kwargs):
        self._generate_users()
        self._generate_todolists()
        self._generate_todos()
        self._generate_comments()
