import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Создаём нового пользователя, и хешируем ему пароль"""

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PasswordResetRequestAPIView(APIView):
    """Запрос на сброс пароля"""

    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        # Получаем email из запроса
        email = request.data.get("email")

        # Проверяем, существует ли пользователь с таким email

        user = User.objects.get(email=email)

        # Генерируем уникальный токен для сброса пароля
        token = secrets.token_hex(16)

        # Сохраняем токен в поле пользователя
        user.token = token
        user.save()

        # Формируем ссылку для сброса пароля
        host = request.get_host()
        uid = user.id  # Получаем идентификатор пользователя
        url = f"https://{host}/users/reset-password/{uid}/{token}/"  # Ссылка на сброс пароля с токеном

        # Отправляем email с ссылкой для сброса пароля
        send_mail(
            subject="Сброс пароля",
            message=f"Для сброса пароля перейдите по следующей ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "Ссылка для сброса пароля отправлена на ваш email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        # Получаем uid, token и новый пароль из тела запроса
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("new_password")

        # Проверяем, переданы ли все необходимые данные
        if not uid or not token or not password:
            return Response(
                {"error": "Необходимо указать uid, token и новый пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Получаем пользователя или возвращаем 404
        user = get_object_or_404(User, id=uid, token=token)

        # Устанавливаем новый пароль
        user.set_password(password)
        user.token = None  # Убираем токен после использования
        user.save()

        return Response(
            {"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK
        )
