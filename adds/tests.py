from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from adds.models import Ad, Comment


class AdAndCommentAPITests(APITestCase):
    def setUp(self):
        """Настройка фикстуры для тестов всех методов"""

        # Создаем обычного пользователя
        self.user = User(
            email="user@example.com", first_name="Иван", last_name="Иванов", role="user"
        )
        self.user.set_password("P4$$W0RD")  # Хешируем пароль
        self.user.save()  # Сохраняем пользователя в базе данных

        # Создаем администратора
        self.admin_user = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role="admin",
        )
        self.admin_user.set_password(
            "adminpassword"
        )  # Хешируем пароль для администратора
        self.admin_user.save()  # Сохраняем администратора в базе данных

        # Данные объявления
        self.ad_data = {
            "title": "Тестовое объявление",
            "price": 1000,
            "description": "Описание тестового объявления",
        }

        # Создаем объявление
        self.ad = Ad.objects.create(**self.ad_data, author=self.user)

        # URL для создания объявления и комментариев
        self.create_ad_url = reverse("ads-list")  # URL для создания объявления
        self.create_comment_url = reverse(
            "comments-list", args=[self.ad.id]
        )  # URL для создания комментария

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_ad(self):
        """Тест на создание объявления"""

        response = self.client.post(self.create_ad_url, self.ad_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Ad.objects.filter(title=self.ad_data["title"]).exists())

    def test_get_ad_list(self):
        """Тест на получение списка объявлений"""

        response = self.client.get(self.create_ad_url)  # Получаем список объявлений

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 4
        )  # Проверяем количество объявлений в ответе

    def test_get_single_ad(self):
        """Тест на получение одного объявления"""

        response = self.client.get(
            reverse("ads-detail", args=[self.ad.id])
        )  # Получаем URL для конкретного объявления

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"], self.ad.title
        )  # Проверяем, что данные совпадают

    def test_update_ad(self):
        """Тест на редактирование своего объявления"""

        updated_data = {
            "title": "Обновленное название",
            "price": 2000,
            "description": "Обновленное описание",
        }

        response = self.client.patch(
            reverse("ads-detail", args=[self.ad.id]), updated_data
        )

        self.ad.refresh_from_db()  # Обновляем объект из базы данных

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.ad.title, updated_data["title"]
        )  # Проверяем обновленное название

    def test_delete_ad(self):
        """Тест на удаление своего объявления"""

        response = self.client.delete(reverse("ads-detail", args=[self.ad.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Ad.objects.filter(id=self.ad.id).exists()
        )  # Проверяем, что объявление удалено

    def test_create_comment(self):
        """Тест на создание комментария"""

        data = {"text": "Это мой комментарий."}

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(text=data["text"]).exists())

    def test_get_comments(self):
        """Тест на получение списка комментариев"""

        Comment.objects.create(
            text="Первый комментарий", author=self.user, ad=self.ad
        )  # Создаем комментарий

        response = self.client.get(
            self.create_comment_url
        )  # Получаем список комментариев

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 4
        )  # Проверяем количество комментариев в ответе

    def test_delete_comment(self):
        """Тест на удаление комментария"""

        # Создаем комментарий
        comment = Comment.objects.create(
            text="Удаляемый комментарий", author=self.user, ad=self.ad
        )

        # Получаем URL для удаления комментария
        delete_url = reverse("comments-detail", args=[self.ad.id, comment.id])

        # Выполняем DELETE-запрос
        response = self.client.delete(delete_url)

        # Проверяем статус ответа и отсутствие комментария в базе данных
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Comment.objects.filter(id=comment.id).exists()
        )  # Проверяем, что комментарий удален
