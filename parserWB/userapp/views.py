from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegistarationForm
from django.views.generic import CreateView
from .models import ParserUser


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'userapp/login.html'


class UserCreateView(CreateView):
    model = ParserUser
    template_name = 'userapp/registration.html'
    form_class = RegistarationForm
    success_url = reverse_lazy('user:login')