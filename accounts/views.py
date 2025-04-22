from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import User


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )


        is_admin = email.endswith('@admin.com')
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=is_admin,
            is_superuser=is_admin
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': is_admin
                },
                'message': 'Registration successful!'
            },
            status=status.HTTP_201_CREATED
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'is_staff': self.user.is_staff
            },
            'message': 'Login successful!'
        })

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.validated_data['user']['is_staff']:
            response = redirect(reverse('admin:index'))
            response.set_cookie(
                'access_token',
                serializer.validated_data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return response

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            {
                'message': f'Hello {request.user.username}!',
                'user_data': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'is_staff': request.user.is_staff
                }
            },
            status=status.HTTP_200_OK
        )
