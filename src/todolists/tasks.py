from anymail.exceptions import AnymailError
from django.apps import apps
from django.contrib.auth.models import User

from accounts.models import Profile
from app.celery import celery


@celery.task(autoretry_for=(AnymailError,), retry_kwargs={'max_retries': 3})
def send_email_about_invitation_to_todolist(caller_user_id, callee_user_id, todolist_id):
    todolist = apps.get_model('todolists.TodoList').objects.get(id=todolist_id)
    caller_user = User.objects.get(id=caller_user_id)
    callee_profile = Profile.objects.get(user_id=callee_user_id)

    callee_profile.send_email_about_invitation_to_todolist(caller_user, todolist)


@celery.task(autoretry_for=(AnymailError,), retry_kwargs={'max_retries': 3})
def send_email_about_excludation_from_todolist(caller_user_id, callee_user_id, todolist_id):
    todolist = apps.get_model('todolists.TodoList').objects.get(id=todolist_id)
    caller_user = User.objects.get(id=caller_user_id)
    callee_profile = Profile.objects.get(user_id=callee_user_id)

    callee_profile.send_email_about_excluding_from_todolist(caller_user, todolist)
