from django.db import models
from userapp.models import ParserUser


# Create your models here.
class TimeStamp(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Product(TimeStamp):
    category = models.CharField(max_length=100)
    article = models.CharField(max_length=50, unique=True)
    rating = models.FloatField()
    review_count = models.IntegerField()
    price = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name


class Category(TimeStamp):

    def __str__(self):
        return self.name


class Tag(TimeStamp):

    def __str__(self):
        return self.name


class Post(TimeStamp):
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    user = models.ForeignKey(ParserUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.name