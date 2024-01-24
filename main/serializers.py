from email.policy import default
from rest_framework import serializers

from users.models import User
from .models import Post, Reaction, Comment


class NestedUserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class PostListSerializer(serializers.ModelSerializer):
    author = NestedUserShortSerializer(label="Информация об авторе")
    content = serializers.SerializerMethodField(label="Краткое содержание")

    class Meta:
        model = Post
        fields = [
            "author",
            "title",
            "content",
            "created_at",
        ]

    def get_content(self, obj):
        max_length = 128
        if len(obj.content) > max_length:
            return obj.content[: max_length - 3] + "..."
        else:
            return obj.content


class PostRetriveSerializer(serializers.ModelSerializer):
    author = NestedUserShortSerializer(label="Информация об авторе")
    self_reaction = serializers.SerializerMethodField(label="Реакции")

    class Meta:
        model = Post
        fields = [
            "author",
            "title",
            "content",
            "comments",
            "self_reaction",
            "created_at",
        ]

    def get_self_reaction(self, obj):
        reaction = self.context["request"].user.reactions.filter(post=obj).first()
        return reaction


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), label="Автор"
    )

    class Meta:
        model = Post
        fields = ["author", "title", "content"]
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'GET':
            fields['author'] = NestedUserShortSerializer(read_only=True, label="Автор")
        return fields

    class Meta:
        model = Comment
        fields = [
            "author",
            "post", 
            "content", 
            "created_at",
            ]
