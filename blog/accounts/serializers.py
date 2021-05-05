from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user()
        fields = ['id', 'username', 'email', 'password']
