from rest_framework import serializers
from django.contrib.auth import get_user_model as user, authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user()
        fields = ['id', 'username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(write_only=True)
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = user()
        fields = ['username', 'password']

    def validate(self, data):
        """
        Validates user data.
        """
        _username = data.get('username', None)
        _password = data.get('password', None)

        if _username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )

        if _password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        _user = authenticate(username=_username, password=_password)

        if _user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not _user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        return _user

class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = user()
        fields = []


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=1,
        write_only=True,
    )
    class Meta:
        model = user()
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        return user().objects.create_user(**validated_data)
