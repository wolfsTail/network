from rest_framework.routers import SimpleRouter

from .views import ChatViewset


communication_router = SimpleRouter()
communication_router.register(r'chats', ChatViewset, basename='chats')
