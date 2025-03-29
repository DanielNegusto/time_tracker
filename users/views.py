from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Представление для регистрации пользователей.

    Это представление обрабатывает регистрацию новых пользователей. Оно принимает данные пользователя,
    проверяет их с помощью UserSerializer, создает нового пользователя и генерирует
    токен аутентификации для только что зарегистрированного пользователя.

    Атрибуты:
        queryset (QuerySet): Запрос для модели User.
        serializer_class (Serializer): Класс сериализатора, используемый для проверки
            и сериализации данных пользователя.

    Методы:
        create(request, *args, **kwargs):
            Обрабатывает POST-запросы для создания нового пользователя и генерации токена аутентификации.

    Запрос:
        POST /api/register/
        {
            "username": "example_user",
            "password": "example_password",
            "email": "user@example.com"
        }

    Ответ:
        В случае успеха:
            HTTP 201 Created
            {
                "token": "сгенерированный_токен"
            }

        В случае ошибки:
            HTTP 400 Bad Request
            {
                "non_field_errors": ["Сообщение об ошибке"]
            }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
