import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
DEBUG = os.getenv('DEBUG', 'False') == 'True'


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'allauth',
    'channels',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'auth_app',
    'meetings',
    'notifications',
    'users',
    'chat',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"',
        }
    },
    'USE_SESSION_AUTH': False,  # Hide Django's default login
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Added for django-allauth
]

ROOT_URLCONF = 'unio_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
   }
}
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "users.User"
# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Django-Allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Optional: Skip for simplicity

# Social account providers (replace with your actual credentials)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': ['openid', 'profile', 'email'],  # Add 'openid' for ID token
        'AUTH_PARAMS': {
            'access_type': 'offline',  # For refresh token
            'prompt': 'consent'  # Force consent for new scopes
        },
    },
    # Microsoft remains the same
    'microsoft': {
        'APP': {
            'client_id': os.getenv('MICROSOFT_CLIENT_ID'),
            'secret': os.getenv('MICROSOFT_SECRET'),
            'key': ''
        },
        'SCOPE': ['User.Read', 'openid', 'profile', 'email'],  # OpenID for ID token
        'TENANT': 'common',
    }
}
if os.getenv("RENDER"):
    load_dotenv("/etc/secrets/DOTENV")   # Render secret file path
else:
    load_dotenv(BASE_DIR / ".env")

ROOT_URLCONF = 'UNIO.urls'               # <-- project-level urls.py
WSGI_APPLICATION = 'UNIO.wsgi.application'

