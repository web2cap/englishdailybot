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
    "tgpages",
    "words",
    "core",
    "api",
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
        "ENGINE": os.getenv("POSTGRES_ENGINE"),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
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
    # "PAGE_SIZE": 30,
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        # "django.db.backends": {
        #     "level": "DEBUG",
        #     "handlers": ["console"],
        # },
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
# logging.basicConfig(level=logging.DEBUG)


TRANSLATOR_FROM = "en"
TRANSLATOR_TO = "ru"

DICT_URL = os.getenv("DICT_URL")
DICT_PAHT = os.getenv("DICT_PAHT")

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
    "tg_id_update_forbidden": "tg_id update forbidden.",
}
