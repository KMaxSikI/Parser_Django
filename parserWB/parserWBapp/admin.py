from django.contrib import admin
from .models import Product, Category, Tag, Post


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Product)