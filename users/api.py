from rest_framework.routers import SimpleRouter

from .views import  UserListViewSet


users_router = SimpleRouter()
users_router.register(r'users', UserListViewSet, basename='users')