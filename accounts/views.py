from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Check if a user with the same username or email already exists
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if User.objects.filter(username=username).exists():
                return Response({'username': 'A user with that username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'email': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            response_data = {
                'username': username,
                'email': email,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
