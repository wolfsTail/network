from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    PostListSerializer, 
    PostRetriveSerializer, 
    PostCreateUpdateSerializer, 
    CommentSerializer,
    ReactionSerializer,
    )
from .models import Post, Comment


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostRetriveSerializer
        else:
            return PostCreateUpdateSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("You can't update this post")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can't delete this post")
        instance.delete()
    
    
class CommentViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ["post__id",]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can't delete this comment")
        instance.delete()


class ReactionViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = ReactionSerializer
