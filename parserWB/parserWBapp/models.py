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
