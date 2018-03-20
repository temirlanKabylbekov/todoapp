from rest_framework import serializers

from todolists.models import TodoList
from todos.api.serializers import TodoFastSerializer


class TodoListSerializer(serializers.ModelSerializer):

    todos = TodoFastSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = [
            'id',
            'name',
            'accessed_users',
            'todos',
        ]


class TodoListUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoList
        fields = [
            'id',
            'name',
        ]


class TodoListCreateSerializer(TodoListUpdateSerializer):

    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta(TodoListUpdateSerializer.Meta):
        fields = TodoListUpdateSerializer.Meta.fields + ['author']
