from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserListSerializer, 
    UserRetrieveSerializer, 
    UserProfileSerializer
    )


class UserListViewSet(
    CreateModelMixin, 
    ListModelMixin,
    RetrieveModelMixin, 
    GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'retrieve':
            return UserRetrieveSerializer
        if self.action == 'me':
            return UserProfileSerializer
        return UserListSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = User.objects.all().prefetch_related('friends').order_by('-id')
        return queryset

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)  

    @action(detail=True, methods=["get"], url_path="friends")
    def friends(self, request, pk=None):
        user = self.get_object()
        queryset = self.filter_queryset(
            self.get_queryset().filter(friends=user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], url_path="add-friend")
    def add_friend(self, request, pk=None):
        user = self.get_object()
        request.user.friends.add(user)
        return Response("Friend added")
    
    @action(detail=True, methods=["post"], url_path="remove-friend")
    def remove_friend(self, request, pk=None):
        user = self.get_object()
        request.user.friends.remove(user)
        return Response("Friend removed")
