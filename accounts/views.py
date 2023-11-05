import jwt
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, ViewProfileSerializer, EditProfileSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Check if a user with the same username or email already exists
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if User.objects.filter(username=username).exists():
                return Response({'username': 'A user with that username already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'email': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            response_data = {
                'username': username,
                'email': email,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @permission_classes([IsAuthenticated])
    def get(self, request):
        custom_token = request.META.get('HTTP_AUTHORIZATION')
        custom_token = custom_token.split(' ')[1]
        custom_token = jwt.decode(custom_token, verify=False)
        print(str(custom_token))

        response_data = {
            'email': custom_token['email'],
            'user_id': custom_token['user_id'],
            'username': custom_token['username'],
            'full_name': custom_token['full_name'],
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ViewProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = EditProfileSerializer(user, data=request.data, partial=True, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return redirect('/accounts/profile/view/')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
