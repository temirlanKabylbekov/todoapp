from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from app.api.views import MultiSerializerMixin
from todos.api import filters, serializers
from todos.models import Todo


class TodoViewset(MultiSerializerMixin, viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = serializers.TodoSerializer
    serializer_action_classes = {
        'retrieve': serializers.TodoDetailSerializer,
    }

    filter_class = filters.TodoFilterSet

    def get_queryset(self):
        return Todo.objects.for_viewset(self.request.user)

    def create(self, *args, **kwargs):
        raise MethodNotAllowed('post', detail='use post: `/api/v1/lists/{pk}/` to create todo')
