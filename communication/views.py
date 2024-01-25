from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Case, When, CharField, Value

from .serializers import ChatSerializer, MessageListSerializer


class ChatViewset(CreateModelMixin, GenericViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.cation == "messages":
            return MessageListSerializer
        return ChatSerializer
    
    @action(detail=True, methods=["get"], url_path="messages")
    def messages(self, request, pk=None):
        messages = self.get_object().messages.filter(chat__id=pk).annotate(
            message_author=Case(
                When(author=self.request.user, then=Value("me"))
                default=F("author__first_name"),
                output_field=CharField(),
            )
        ).order_by("created_at")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)