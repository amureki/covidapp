import os
import secrets
from datetime import timedelta
from pathlib import Path

import environ
import sentry_sdk
from configurations import Configuration, values
from sentry_sdk.integrations.django import DjangoIntegration

from . import heroku

env = environ.Env()

_release = heroku.RELEASE[1:]
_commit = heroku.COMMIT[:8]
_environment = (
    heroku.APP_NAME.replace("covid19", "")[1:] or "production"
    if heroku.APP_NAME
    else "dev"
)


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    ALLOWED_HOSTS = []

    CACHES = {
        "default": env.cache("CACHE_URL", "redis://127.0.0.1:6379/0"),
        "sessions": env.cache("SESSIONS_URL", "redis://127.0.0.1:6379/1"),
    }
    CACHE_MIDDLEWARE_SECONDS = values.IntegerValue(
        environ_prefix="", default=60 * 60 * 24
    )

    DATABASES = {
        "default": env.db(default="postgres://localhost/covid19?conn_max_age=600"),
    }

    DEBUG = False

    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.postgres",
        "django.contrib.staticfiles",
        "django.contrib.humanize",
        "django_extensions",
        "rest_framework",
        "drf_yasg",
        "data",
    ]

    LANGUAGE_CODE = "en-us"

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.middleware.cache.UpdateCacheMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.cache.FetchFromCacheMiddleware",
    ]

    ROOT_URLCONF = "core.urls"

    SECRET_KEY = values.SecretValue()

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "sessions"

    SITE_ID = 1
    SITE_URL = env("SITE_URL", default="https://covidapp.herokuapp.com/")

    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATIC_URL = "/static/"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.csrf",
                ],
            },
        },
    ]

    TIME_ZONE = "Europe/Berlin"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    WSGI_APPLICATION = "core.wsgi.application"

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            "OPTIONS": {"min_length": 9,},
        },
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
    ]

    REST_FRAMEWORK = {
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    }


class Development(Common):
    DEBUG = True
    SECRET_KEY = "secret_key"

    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": (
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ),
    }


class Test(Common):
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

    SECRET_KEY = Development.SECRET_KEY


class Production(Common):
    ALLOWED_HOSTS = values.ListValue(environ_prefix="", default=[])

    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

    MIDDLEWARE = [
        "django.middleware.http.ConditionalGetMiddleware",
        "django.middleware.gzip.GZipMiddleware",
    ] + Common.MIDDLEWARE

    SENTRY_CONFIG = {
        "dsn": os.getenv("SENTRY_DSN", ""),
        "environment": _environment,
        "release": _release,
    }

    @classmethod
    def post_setup(cls):
        super().post_setup()
        sentry_sdk.init(
            integrations=[DjangoIntegration()],
            **cls.SENTRY_CONFIG,
            send_default_pii=True
        )
