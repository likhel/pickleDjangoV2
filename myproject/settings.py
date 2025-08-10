from decouple import config
from pathlib import Path
import os
from datetime import timedelta # Import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use decouple to load SECRET_KEY from your .env file
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Use decouple to load DEBUG from your .env file
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required for allauth

    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google', # Uncomment if you are using Google social login
    'django_countries',
    'phonenumber_field',
    'corsheaders',
    'user',
    'order',
    'product', 
    # 'payment', # Uncomment if you have these apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Add CorsMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Add AccountMiddleware for allauth
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = 'user.CustomUser'

SITE_ID = 1 # Required by django.contrib.sites and allauth

# Allauth settings
# ACCOUNT_AUTHENTICATION_METHOD = 'email'  Use email for authentication
ACCOUNT_LOGIN_METHODS = ['email']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'first_name', 'last_name'] # Specify the fields required during signup
# # Set to True if you want users to enter email twice

ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_USERNAME_REQUIRED = False # Assuming you are not using usernames
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # 'mandatory' or 'optional' or 'none'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True # Confirm email on GET request to the verification link
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Your Site Name] ' # Subject prefix for emails
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' # Use 'https' in production
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3 # Number of days the confirmation link remains valid
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True # Use HMAC for email confirmation tokens
ACCOUNT_LOGIN_ATTEMPT_LIMIT = 5 # Limit failed login attempts
ACCOUNT_LOGIN_ATTEMPT_TIMEOUT = 300 # Lockout time in seconds after reaching limit

# Redirect URLs after login, logout, and email confirmation
LOGIN_REDIRECT_URL = '/' # Or your desired redirect URL
ACCOUNT_LOGOUT_REDIRECT_URL = '/' # Or your desired redirect URL
ACCOUNT_EMAIL_CONFIRMATION_REDIRECT_URL = '/' # Or your desired redirect URL after email confirmation

# Email settings (required for sending verification emails)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Use console backend for testing
# In production, configure your actual email backend (e.g., SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# dj-rest-auth settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication', # Remove or comment out SessionAuthentication
        'rest_framework.authentication.BasicAuthentication', # Keep if you use BasicAuthentication
        'rest_framework_simplejwt.authentication.JWTAuthentication', # Add JWT Authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Or your desired default permission
    ),
    # ... other DRF settings
}

REST_AUTH = {
    'USE_JWT': True,  # Enable JWT
    'SESSION_LOGIN': False,  # Disable session login
    'REGISTER_SERIALIZER': 'user.serializers.UserRegistrationSerializer',
    # 'LOGIN_SERIALIZER': 'user.serializers.UserLoginSerializer', # Remove this line
    'USER_DETAILS_SERIALIZER': 'user.serializers.UserSerializer',
    # 'JWT_AUTH_COOKIE': 'my-app-auth', # Optional: Use a cookie for JWT
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token', 
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializers.UserRegistrationSerializer',
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Lifetime of the access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Lifetime of the refresh token
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # Use your project's SECRET_KEY for signing
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True