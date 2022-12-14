"""
Django settings for toolkit project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_dramatiq",
]

CUSTOM_APPS = [
    "account",
    "common",
    "stock",
    "wechat",
]

INSTALLED_APPS.extend(CUSTOM_APPS)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "toolkit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "toolkit.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", 0)),
    }
}

# Dramatiq
# https://github.com/Bogdanp/django_dramatiq
# todo: ????????????
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": os.getenv("DRAMATIQ_RABBITMQ_URL", ""),
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": "redis://localhost:6379",
    },
    "MIDDLEWARE_OPTIONS": {"result_ttl": 60000},
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "/collectstatic"

# https://docs.djangoproject.com/zh-hans/4.0/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.User"

# admin???????????????
USE_L10N = False
DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"

# Django REST framework ??????
# https://www.django-rest-framework.org/api-guide/settings/#settings
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%s",
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": (
        # ????????????????????????
        "toolkit.middleware.renderers.UniformJSONRenderer",
    ),
    # ??????????????????
    "EXCEPTION_HANDLER": "toolkit.middleware.handlers.exception_handler",
    "DEFAULT_PERMISSION_CLASSES": (
        # ???????????????????????????token??????
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # ??????csrf??????
        "toolkit.middleware.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        # django-filter ?????? rest_framework
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
}

# ?????????????????????
# https://docs.djangoproject.com/zh-hans/4.1/topics/logging/#configuring-logging
# [????????????] [????????????] [??????ID ?????????] [?????????] [??????] - ????????????
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)-4s] [%(process)d %(threadName)s] [%(name)s] [%(lineno)d] - %(message)s"

LOG_CONFIG = {
    "handlers": ["console"],
    "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    "propagate": False,
}
DB_LOG_CONFIG = {
    "handlers": ["console"],
    "level": os.getenv("DJANGO_DB_LOG_LEVEL", "ERROR"),
    "propagate": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOGGING_FORMAT},
    },
    "handlers": {
        "console": {
            "formatter": "verbose",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": LOG_CONFIG,
        "django.db": DB_LOG_CONFIG,
        **{app: LOG_CONFIG for app in CUSTOM_APPS},
    },
}
