from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "telegram_chat_id"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            telegram_chat_id=validated_data.get("telegram_chat_id"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
