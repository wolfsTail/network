from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Q, Case, OuterRef, Subquery, When, CharField, Value
from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatListSerializer, ChatSerializer, MessageListSerializer, MessageSerializer


class ChatViewset(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet):

    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == "messages":
            return MessageListSerializer
        if self.action == "list":
            return ChatListSerializer
        return ChatSerializer

    def get_queryset(self):
        user = self.request.user

        last_message_subquery = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-created_at').values('created_at')[:1]
        last_message_content_subquery = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-created_at').values('text')[:1]

        qs = Chat.objects.filter(
            Q(user_1=user) | Q(user_2=user),
            messages__isnull=False,
        ).annotate(
            last_message_datetime=Subquery(last_message_subquery),
            last_message_content=Subquery(last_message_content_subquery),
        ).select_related(
            "user_1",
            "user_2",
        ).order_by("-last_message_datetime").distinct()
        return qs
    
    @action(detail=True, methods=["get"], url_path="messages")
    def messages(self, request, pk=None):
        messages = self.get_object().messages.filter(chat__id=pk).annotate(
            message_author=Case(
                When(author=self.request.user, then=Value("me")),
                default=F("author__first_name"),
                output_field=CharField(),
            )
        ).order_by("created_at")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


class MessageViewset(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet):

    permission_classes = [IsAuthenticated,]
    serializer_class = MessageSerializer
    queryset = Message.objects.all().order_by("-created_at")

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can't delete this message")
        instance.delete()