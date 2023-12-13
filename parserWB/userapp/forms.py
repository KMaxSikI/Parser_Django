from django.contrib.auth.forms import UserCreationForm
from .models import ParserUser


class RegistarationForm(UserCreationForm):
    class Meta:
        model = ParserUser
        fields = ('username', 'password1', 'password2', 'email')
