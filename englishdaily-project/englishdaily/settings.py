import os
import logging

from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = True
if DEBUG is True:
    ALLOWED_HOSTS = ["*"]
# TODO:
else:
    ALLOWED_HOSTS = [os.getenv("TELEGRAM_BOT_SERVER")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "bot",
    "words",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "users.User"

ROOT_URLCONF = "englishdaily.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "englishdaily.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PREFIX = os.getenv("REDIS_PREFIX")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # "DEFAULT_PAGINATION_CLASS": "api.pagination.CustomPagination",
    # "PAGE_SIZE": 5,
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TRANSLATOR_FROM = "en"
TRANSLATOR_TO = "ru"

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")
TELEGRAM_BOT_SERVER = os.getenv("TELEGRAM_BOT_SERVER")
TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL")

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    f"https://{TELEGRAM_BOT_SERVER}",
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MESSAGES = {
    "bot_unregistred": "Bot URL was unregistred on TG server.",
    "bot_registred": "Bot URL was registred on TG server.",
}

logging.basicConfig(level=logging.DEBUG)
