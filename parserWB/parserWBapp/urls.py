from django.urls import path
from parserWBapp import views

app_name = 'parserWBapp'

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('parse/', views.parse_form, name='parse_form'),  # Страница с формой для парсинга
    path('parse/results/', views.parse_results, name='parse_results'),  # Страница с результатами парсинга
    path('posts/<int:id>/', views.posts, name='posts'),  # Страница с постами
]