from django.db import models

from app.models import TimestampedModel


class Comment(TimestampedModel):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()
    todo = models.ForeignKey('todos.Todo', on_delete=models.CASCADE, related_name='comments', null=True)

    def __str__(self):
        return '%s | %s' % (self.author, self.todo)
