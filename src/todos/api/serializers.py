from rest_framework import serializers

from comments.api.serializers import CommentTodoSerializer
from todos.models import Todo


class TodoFastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
        ]


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'due_date',
            'description',
            'is_important',
            'has_completed',
            'assigned',
            'todolist',
        ]
        extra_kwargs = {'title': {'required': False}}


class TodoDetailSerializer(TodoSerializer):

    comments = CommentTodoSerializer(many=True)

    class Meta(TodoSerializer.Meta):
        fields = TodoSerializer.Meta.fields + ['comments']
