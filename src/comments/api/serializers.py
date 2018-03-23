from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from accounts.api.serializers import UserSerializer
from comments.models import Comment
from todos.models import Todo


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'text']


class CommentCreateSerializer(CommentUpdateSerializer):

    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta(CommentUpdateSerializer.Meta):
        fields = CommentUpdateSerializer.Meta.fields + ['author', 'todo']
        extra_kwargs = {'todo': {'allow_null': False}}

    def validate(self, data):
        if data['todo'] not in Todo.objects.available_to_user(data['author']):
            raise PermissionDenied('you cant post comment for not available todo')
        return data


class CommentTodoSerializer(serializers.ModelSerializer):

    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ['author', 'text']
