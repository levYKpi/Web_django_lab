from rest_framework import generics
from rest_framework import status
from . import serializers
from django.contrib.auth import get_user_model as user, login, logout

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

from blog.celery import app
import logging
from django.core.mail import send_mail


@app.task
def sending_mail(email):
    try:
        send_mail(
            'you have logged into your account',
            'from blog_app: %s' % email,
            'from@admin.com',
            [email],
            fail_silently=False,
        )
    except Exception as e:
        logging.warning(e)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    # queryset = user().objects.all()
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        _user = user().objects.get(id=serializer.data['id'])
        login(user=_user, request=request)
        print("user:", _user)
        sending_mail.delay(email=str(_user))
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    # queryset = user().objects.all()
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        logout(request=request)
        return Response(status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    queryset = user().objects.all()
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoggedView(generics.GenericAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.LoggedSerializer

    def get(self, request):
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
        return Response(data=user().objects.filter(id__in=uid_list[1:]).values(), status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user().objects.all()
    serializer_class = serializers.UserSerializer
