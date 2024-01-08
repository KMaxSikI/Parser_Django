from django.test import TestCase
from .models import Post, Category, Product, Tag
from userapp.models import ParserUser
from mixer.backend.django import mixer


class TestModels(TestCase):

    def test_product_model(self):
        product = mixer.blend(Product,
                              category="Electronics",
                              article="12345",
                              rating=4.5,
                              review_count=100,
                              price="99.99",
                              url="https://example.com")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.article, "12345")
        self.assertAlmostEqual(product.rating, 4.5)
        self.assertEqual(product.review_count, 100)
        self.assertEqual(product.price, "99.99")
        self.assertEqual(product.url, "https://example.com")

    def test_category_model(self):
        category = mixer.blend(Category, name="Technology")
        self.assertEqual(category.name, "Technology")

    def test_tag_model(self):
        tag = mixer.blend(Tag, name="Python")
        self.assertEqual(tag.name, "Python")

    def test_post_model(self):
        category = mixer.blend(Category, name="Technology")
        tag = mixer.blend(Tag, name="Python")
        user = mixer.blend(ParserUser)
        post = mixer.blend(Post, category=category, tags=[tag], user=user, text="Sample text")

        self.assertEqual(post.category.name, "Technology")
        self.assertEqual(post.tags.first().name, "Python")
        self.assertEqual(post.user, user)
        self.assertEqual(post.text, "Sample text")