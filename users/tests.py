from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserAPITests(APITestCase):
    def setUp(self):
        """Настройка фикстуры для тестов всех методов"""
        self.user_data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivan@example.com",
            "password": "P4$$W0RD",
            "phone": "1234567890",
            "role": "user"
        }
        self.create_url = reverse('users:register')
        self.reset_password_request_url = reverse('users:reset_password_request')
        self.reset_password_confirm_url = reverse('users:reset_password_confirm')

    def test_create_user(self):
        """Тест на создание пользователя"""
        response = self.client.post(self.create_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_password_reset_request(self):
        """Тест на запрос сброса пароля"""
        user = User(
            first_name="Иван",
            last_name="Иванов",
            email=self.user_data["email"],
            phone=self.user_data["phone"],
            role=self.user_data["role"],
            is_active=True  # Убедитесь, что пользователь активен
        )
        user.set_password(self.user_data["password"])  # Хешируем пароль
        user.save()

        response = self.client.post(self.reset_password_request_url, {"email": self.user_data["email"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Ссылка для сброса пароля отправлена на ваш email.", response.data["message"])

    def test_password_reset_confirm(self):
        """Тест на подтверждение сброса пароля"""
        user = User(
            first_name="Иван",
            last_name="Иванов",
            email=self.user_data["email"],
            phone=self.user_data["phone"],
            role=self.user_data["role"],
            is_active=True
        )
        user.set_password(self.user_data["password"])  # Хешируем пароль
        user.save()

        # Генерация токена (в реальном сценарии это должно происходить в методе сброса пароля)
        token = 'testtoken'  # Пример токена для теста
        user.token = token
        user.save()

        new_password = "NewP4$$W0RD"

        response = self.client.post(self.reset_password_confirm_url, {
            "uid": user.id,
            "token": token,
            "new_password": new_password
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()  # Обновляем объект пользователя из базы данных
        self.assertTrue(user.check_password(new_password))  # Проверяем новый пароль
