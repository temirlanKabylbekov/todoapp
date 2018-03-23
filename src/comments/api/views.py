from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.api.views import MultiSerializerMixin
from comments.api import serializers
from comments.models import Comment


class CommentViewset(MultiSerializerMixin, viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = serializers.CommentSerializer
    serializer_action_classes = {
        'create': serializers.CommentCreateSerializer,
        'update': serializers.CommentUpdateSerializer
    }

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('id')
