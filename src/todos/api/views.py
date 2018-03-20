from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from todos.api import serializers
from todos.models import Todo


class TodoViewset(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TodoSerializer

    def get_queryset(self):
        return Todo.objects.for_viewset(self.request.user)

    def create(self, *args, **kwargs):
        raise MethodNotAllowed('post', detail='use post: `/api/v1/lists/{pk}/` to create todo')
