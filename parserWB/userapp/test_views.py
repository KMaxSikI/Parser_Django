from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserLoginViewTest(TestCase):
    def test_login_view(self):
        # Создаем тестового пользователя
        user = get_user_model().objects.create_user(username='testuser', email='test@example.com',
                                                    password='testpassword')

        # Имитируем запрос к представлению для входа в систему
        client = Client()
        response = client.post(reverse('user:login'), {'username': 'testuser', 'password': 'testpassword'})

        # Проверяем, что пользователь успешно вошел в систему
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после входа


class UserCreateViewTest(TestCase):
    def test_create_user_view(self):
        # Имитируем запрос к представлению регистрации
        client = Client()
        response = client.post(reverse('user:registration'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword4517', 'password2': 'newpassword4517'})

        # Проверяем, что пользователь был успешно создан и перенаправлен на страницу входа
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после успешной регистрации
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())  # Проверяем, что пользователь создан