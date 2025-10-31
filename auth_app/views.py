from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from allauth.socialaccount.models import SocialAccount
from allauth.account.utils import perform_login
from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from users.models import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging
from rest_framework_simplejwt.views import TokenRefreshView

logger = logging.getLogger(__name__)
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

# Utility to create JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RefreshView(TokenRefreshView):
    """Custom JWT token refresh endpoint"""
    pass

# =====================================
# Signup
# =====================================
class SignupView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        )
    )
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        tokens = get_tokens_for_user(user)
        return Response({'message': 'User created', **tokens}, status=status.HTTP_201_CREATED)

# =====================================
# Login (Username / Password)
# =====================================
class LoginView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        )
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)

# =====================================
# Google Login
# =====================================
class GoogleLoginView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id_token': openapi.Schema(type=openapi.TYPE_STRING)},
            required=['id_token']
        )
    )
    def post(self, request):
        token_value = request.data.get('id_token')
        try:
            info = id_token.verify_oauth2_token(token_value, google_requests.Request(), GOOGLE_CLIENT_ID)
            email = info.get('email')
            user, _ = User.objects.get_or_create(email=email, defaults={'username': email.split('@')[0]})
            SocialAccount.objects.update_or_create(
                user=user, provider='google', uid=info['sub'], defaults={'extra_data': info}
            )
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Invalid token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

# =====================================
# Microsoft Login
# =====================================
class MicrosoftLoginView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'access_token': openapi.Schema(type=openapi.TYPE_STRING)},
            required=['access_token']
        )
    )
    def post(self, request):
        access_token = request.data.get('access_token')
        adapter = MicrosoftGraphOAuth2Adapter(request)
        try:
            provider = adapter.get_provider()
            app = provider.app

            class Token:
                def __init__(self, value): self.token = value

            token = Token(access_token)
            social_login = adapter.complete_login(request, app=app, token=token, response={})
            user = social_login.user
            user.save()
            SocialAccount.objects.update_or_create(
                user=user, provider='microsoft', uid=social_login.account.uid,
                defaults={'extra_data': social_login.account.extra_data}
            )
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'OAuth error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

# =====================================
# Logout
# =====================================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
