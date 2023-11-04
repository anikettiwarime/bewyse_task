from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=100,
        error_messages={
            'required': 'Password is required',
            'min_length': 'This password is too short. It must contain at least 8 characters',
            'max_length': 'This password is too long. It must contain at most 100 characters',
        }
    )

    email = serializers.EmailField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address',
            'max_length': 'This email is too long. It must contain at most 100 characters',
        }
    )

    username = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            'unique': 'A user with that username already exists',
            'required': 'Username is required',
            'max_length': 'This username is too long. It must contain at most 100 characters',
        }
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
