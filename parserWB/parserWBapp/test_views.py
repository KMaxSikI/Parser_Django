from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from .models import Post, Product, Category
from userapp.models import ParserUser
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = "Sample Category"  # Пример категории для тестов

    def test_parse_form_view(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser1', password='password1234')
        self.client.force_login(user)
        response = self.client.get('/parse/')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что форма присутствует на странице
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="category"')

        # Проверяем выполнение парсинга
        response = self.client.post('/parse/', {'category': self.category})
        self.assertEqual(response.status_code, 302)

    def test_parse_results_view(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser1', password='password1234')
        self.client.force_login(user)

        # Создаем объект Product для проверки его отображения на странице результатов парсинга
        product = Product.objects.create(
            article="12345",
            category=self.category,
            name="Sample Product",
            rating=4,
            review_count=100,
            price="99.99 руб.",
            url="https://www.example.com/product/12345"
        )

        response = self.client.get('/parse/results/')

        self.assertEqual(response.status_code, 200)

        # Проверяем отображение данных модели Product на странице
        self.assertContains(response, product.article)
        self.assertContains(response, product.category)
        self.assertContains(response, product.name)
        self.assertContains(response, str(product.rating))
        self.assertContains(response, str(product.review_count))
        self.assertContains(response, product.price)
        self.assertContains(response, product.url)

    def test_post_detail_view(self):
          # Проверка страницы с постом, содержит ли страница все необходимые данные для поста
        some_category = Category.objects.create(name="Some Category")
        user = ParserUser.objects.create(username='testuser', password='password123')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        post = Post.objects.create(name="Test Post",
                                   text="This is a test post.",
                                   category=some_category,
                                   user=user,
                                   image=image)
        response = self.client.get(f'/posts/{post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")  # Проверяем наличие заголовка поста на странице
        self.assertContains(response, "This is a test post.")  # Проверяем наличие текста поста на странице

    def test_post_create_view_for_authenticated_user(self):
          # Проверка доступа к странице создания поста для авторизованных пользователей:
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_login(user)

        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_view_for_unauthenticated_user(self):
          # Проверяем, что неавторизованный пользователь перенаправляется на страницу входа:
        response = self.client.get('/create/')
        self.assertRedirects(response,
                             '/user/login/?next=/create/')
