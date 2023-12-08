from django import forms
from .models import Post, Category


class ParsForm(forms.Form):
    category = forms.CharField(label='Введите категорию товаров')


class PostForm(forms.ModelForm):
    name = forms.CharField(label='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Введите название поста', 'class': 'form-control w-50'}))

    text = forms.CharField(label='',
                           widget=forms.Textarea(
                               attrs={'placeholder': 'Введите текст поста', 'class': 'form-control'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория поста')

    image = forms.ImageField(label='Картинка для поста', widget=forms.FileInput)

    class Meta:
        model = Post
        fields = ['name', 'text', 'category', 'image']
        labels = {
            'name': 'Название',
            'text': 'Текст',
            'category': 'Категория',
            'image': 'Изображение',
        }
        exclude = ('tags',)
