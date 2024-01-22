from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserRegistrationSerializer, UserListSerializer, UserRetrieveSerializer


class UserListViewSet(
    CreateModelMixin, 
    ListModelMixin,
    RetrieveModelMixin, 
    GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'list':
            return UserListSerializer
        if self.action in ('retrieve', 'me'):
            return UserRetrieveSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




