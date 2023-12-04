from django.db import models


# Create your models here.

class Product(models.Model):
    category = models.CharField(max_length=100)
    article = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    review_count = models.IntegerField()
    price = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=32, unique=True)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='posts', null=True, blank=True)


    def __str__(self):
        return self.name