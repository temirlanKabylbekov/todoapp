from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.api.views import MultiSerializerMixin
from todos.api.serializers import TodoCreateSerializer, TodoSerializer
from todos.models import Todo


class TodoViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    serializer_action_classes = {
        'create': TodoCreateSerializer,
    }

    def get_queryset(self):
        return Todo.objects.available_to_user(self.request.user)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)
