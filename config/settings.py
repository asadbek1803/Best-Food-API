from pathlib import Path
import os
from environs import Env
import dj_database_url
from datetime import timedelta


env = Env()
env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
GRAPHHOPPER_API_KEY = env.str("GRAPHHOPPER_API_KEY", "")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])


# Application definition


STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CORS_ALLOW_ALL_ORIGINS = True  # Ehtiyot bo‘ling, faqat testda ishlating!


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "channels",
    "rest_framework",
    'rest_framework.authtoken',
    "django_filters",
    "modeltranslation",
    "drf_yasg",
    "corsheaders",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    

    
    #Local
    "api",
    "accounts",
    


]


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT autentifikatsiyasi
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # 30 daqiqa yaroqlilik
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # 30 kun yaroqlilik
    "ROTATE_REFRESH_TOKENS": True,  # Har foydalanishda yangilash
    "BLACKLIST_AFTER_ROTATION": True,  # Eski tokenni qora ro‘yxatga kiritish
}

# Django'da ishlatiladigan tillar
LANGUAGES = (
    ('uz', 'Uzbek'),
    ('en', 'English'),
    ('ru', 'Russian'),
)

# ModelTranslation kutubxonasida asosiy til
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
AUTH_USER_MODEL = 'accounts.User'
# Agar Django admin panelida tarjima qilishni xohlasangiz
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Statik va media fayllarni sozlash
STATIC_URL = env.str("STATIC_URL", "/static/")
STATIC_ROOT = BASE_DIR / env.str("STATIC_ROOT", "staticfiles")
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = env.str("MEDIA_URL", "/media/")
MEDIA_ROOT = BASE_DIR / env.str("MEDIA_ROOT", "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
