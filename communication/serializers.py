from django.db.models import Q
from rest_framework import serializers

from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    user_1 = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Chat
        fields = ["user_1", "user_2"]
    
    def create(self, validated_data):
        request_user = validated_data["user_1"]
        response_user = validated_data["user_2"]

        chat = Chat.objects.filter(
            Q(user_1=request_user, user_2=response_user) |
            Q(user_1=response_user, user_2=request_user)
        ).first()

        if not chat:
            chat = Chat.objects.create(user_1=request_user, user_2=response_user)

        return chat


class MessageListSerializer(serializers.ModelSerializer):
    message_author = serializers.CharField(label="Автор сообщения")

    class Meta:
        model = Message
        fields = ["chat", "message_author", "text", "created_at"]