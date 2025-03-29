from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]  # Убрали is_moderator

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
        )
        user.set_password(
            validated_data["password"]
        )  # Храните пароль в зашифрованном виде
        user.save()
        return user
