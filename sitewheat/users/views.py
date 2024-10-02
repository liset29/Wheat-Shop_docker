from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUsersForm, RegisterUserForm
from wheat.models import Basket, Users





class LoginUser(LoginView):
    form_class = LoginUsersForm
    template_name = 'users/login.html'
    extra_context = {'title':'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))