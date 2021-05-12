from django.http.response import HttpResponse
from rest_framework import generics
from rest_framework import status
from . import serializers
from django.contrib.auth import get_user_model as user, login, logout

from django.urls import reverse_lazy
from django.views import generic as dvg

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        login(user=user().objects.get(id=serializer.data['id']), request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        logout(request=request)
        return Response(status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserList(generics.ListCreateAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer
