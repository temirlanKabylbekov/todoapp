from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from comments.api.serializers import CommentTodoSerializer
from todolists.choices import TODO_POSITIONS
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


class TodoPositionsInTodoListSerializer(serializers.Serializer):

    todos = serializers.ListField(child=serializers.IntegerField())

    def validate_todos(self, todo_ids):
        todos = Todo.objects.filter(todolist=self.context['todolist']).order_by('id').values_list('id', flat=True)

        if list(todos) != sorted(todo_ids):
            raise ValidationError('contains strange todo or not all todos passed')

        return todo_ids


class NamedTodoPositionsInTodoListSerializer(serializers.Serializer):

    name = serializers.ChoiceField(choices=TODO_POSITIONS, required=True)
    asc = serializers.BooleanField(default=True)
