from rest_framework import serializers

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
