from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.views import MultiSerializerMixin
from todolists.api import serializers
from todolists.models import TodoList
from todos.api.serializers import (
    NamedTodoPositionsInTodoListSerializer, TodoPositionsInTodoListSerializer, TodoSerializer)


class TodoListViewset(MultiSerializerMixin, viewsets.ModelViewSet):

    queryset = TodoList.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = serializers.TodoListSerializer
    serializer_action_classes = {
        'create': serializers.TodoListCreateSerializer,
        'update': serializers.TodoListUpdateSerializer,
    }

    def get_queryset(self):
        return TodoList.objects.for_viewset(self.request.user)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def todos(self, request, pk=None):
        instance = self.get_object()

        serializer = TodoSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['todolist'] = instance
        todo = serializer.save()

        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)

    def _get_user_to_invite_or_exclude(self, request):
        user_id = request.data.get('id')
        if user_id is None:
            raise ValidationError('you should pass "id" param')
        return get_object_or_404(User, pk=user_id)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def invite_user(self, request, pk=None):
        user = self._get_user_to_invite_or_exclude(request)
        instance = self.get_object()

        try:
            instance.invite_user(request.user, user)
        except DjangoValidationError as e:
            raise ValidationError(e.message)

        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def exclude_user(self, request, pk=None):
        user = self._get_user_to_invite_or_exclude(request)
        instance = self.get_object()

        try:
            instance.exclude_user(request.user, user)
        except DjangoValidationError as e:
            raise ValidationError(e.message)

        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated])
    def todo_positions(self, request, pk=None):
        instance = self.get_object()

        context = self.get_serializer_context()
        context['todolist'] = instance

        serializer = TodoPositionsInTodoListSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        instance.set_todo_order(serializer.validated_data['todos'])

        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated])
    def todo_positions_by_name(self, request, pk=None):
        serializer = NamedTodoPositionsInTodoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        asc = serializer.validated_data['asc']
        getattr(self.get_object(), 'set_todo_order_by_%s' % serializer.validated_data['name'])(asc=asc)

        return Response(status=status.HTTP_200_OK)
