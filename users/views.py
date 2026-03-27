from rest_framework import generics, permissions
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    "Регистрация пользователя"

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
