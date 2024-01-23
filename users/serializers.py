from rest_framework import serializers

from main.models import Post
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class NestedPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [             
            "title", 
            "content", 
            "created_at",
            ]


class UserListSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "is_friend"]

    def get_is_friend(self, obj) -> bool:
        curr_user = self.context["request"].user
        return curr_user in obj.friends.all()


class AbsUserRetrieveSerializer(serializers.ModelSerializer):    
    qty_of_friends = serializers.SerializerMethodField()
    posts = NestedPostListSerializer(many=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username", 
            "first_name", 
            "last_name", 
            "email",            
            "qty_of_friends",
            "posts",
            ]
      
    def get_qty_of_friends(self, obj) -> int:
        return obj.friends.count()


class UserRetrieveSerializer(AbsUserRetrieveSerializer):
    is_friend = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "username", 
            "first_name", 
            "last_name", 
            "email",
            "is_friend",
            "qty_of_friends",
            "posts",
            ]
    
    def get_is_friend(self, obj) -> bool:
        return obj in self.context["request"].user.friends.all()


class UserProfileSerializer(AbsUserRetrieveSerializer):  
    pass