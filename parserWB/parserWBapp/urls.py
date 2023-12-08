from django.urls import path
from parserWBapp import views

app_name = 'parserWBapp'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('parse/', views.ParseFormView.as_view(), name='parse_form'),
    path('parse/results/', views.ParseResultsView.as_view(), name='parse_results'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='posts'),
    path('create/', views.PostCreateView.as_view(), name='create'),
]