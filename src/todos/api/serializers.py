from rest_framework import serializers

from todos.models import Todo


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
        ]


class TodoCreateSerializer(TodoSerializer):

    class Meta(TodoSerializer.Meta):
        fields = TodoSerializer.Meta.fields + ['author']
