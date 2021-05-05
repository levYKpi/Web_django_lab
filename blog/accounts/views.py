from rest_framework import generics
from . import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as dvg

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class RegisterView(dvg.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class UserList(generics.ListCreateAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer
