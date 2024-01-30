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


class ChatListSerializer(serializers.ModelSerializer):
    companion_name = serializers.SerializerMethodField(label="Имя собеседника")
    last_message_content = serializers.SerializerMethodField(label="Текст последнего сообщения")
    last_message_datetime = serializers.DateTimeField(label="Дата и время последнего сообщения")

    class Meta:
        model = Chat
        fields = [
            "companion_name", 
            "last_message_content", 
            "last_message_datetime"
            ]
    
    def get_last_message_content(self, obj) -> str:
        return obj.last_message_content

    def get_companion_name(self, obj) -> str:
        companion = obj.user_1 if obj.user_2 == self.context["request"].user else obj.user_2
        return f"{companion.first_name} {companion.last_name}"
    

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs): 
        chat = attrs["chat"]
        author = attrs["author"]
        if chat.user_1 != author and chat.user_2 != author:
            raise serializers.ValidationError("You are not a part of this chat")
        return super().validate(attrs)
    
    class Meta:
        model = Message
        fields = [
            "chat", 
            "author", 
            "text", 
            "created_at"
            ]
