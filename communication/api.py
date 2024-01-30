from rest_framework.routers import SimpleRouter

from .views import ChatViewset, MessageViewset


communication_router = SimpleRouter()
communication_router.register(r'chats', ChatViewset, basename='chats')
communication_router.register(r'messages', MessageViewset, basename='messages')
