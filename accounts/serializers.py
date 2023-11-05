from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')

        user = User.objects.get(username=username)
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Username or password is invalid')

        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['full_name'] = user.first_name + " " + user.last_name
        token['username'] = user.username
        return token


class ViewProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'full_name': f"{instance.first_name} {instance.last_name}"
        }


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False}
        }

    def validate_username(self, value):
        request = self.context['request']
        user = request.user
        if value == user.username:
            raise serializers.ValidationError({"error": f"No change detected in username."})
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"unique": f"User already exist with the username {value}."})
        return value

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'username' in validated_data:
            instance.username = validated_data['username']
        instance.save()
        return instance
