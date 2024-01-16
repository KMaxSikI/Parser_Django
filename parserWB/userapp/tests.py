from django.test import TestCase
from mixer.backend.django import mixer
from .models import ParserUser


class BlogUserModelTest(TestCase):
    def test_email_field_unique(self):
        # Создаем пользователя с помощью mixer
        mixer.blend(ParserUser, email='pop@test.com')

        # Пытаемся создать еще одного пользователя с тем же email
        with self.assertRaises(Exception):
            mixer.blend(ParserUser, email='pop@test.com')

    def test_is_author_default(self):
        # Создаем пользователя с помощью mixer
        user = mixer.blend(ParserUser)

        # Проверяем, что поле is_author имеет значение по умолчанию False
        self.assertFalse(user.is_author)

    def test_user_creation(self):
        # Создаем пользователя с помощью mixer
        mixer.blend(ParserUser)

        # Проверяем, что пользователь успешно создан
        user_count = ParserUser.objects.count()
        self.assertEqual(user_count, 1)
