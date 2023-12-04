from django import forms


class ParsForm(forms.Form):

    category = forms.CharField(label='Введите категорию товаров')