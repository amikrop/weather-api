import sys
from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env.str("SECRET_KEY", " ")

DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "users",
    "weather",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "weatherapi.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "weatherapi.wsgi.application"

DEFAULT_DB_NAME = (
    ":memory:"
    if "test" in sys.argv or "pytest" in sys.modules
    else BASE_DIR / "db.sqlite3"
)

DATABASES = {
    "default": {
        "ENGINE": env.str("SQL_ENGINE", "django.db.backends.sqlite3"),
        "USER": env.str("SQL_USER", ""),
        "PASSWORD": env.str("SQL_PASSWORD", ""),
        "NAME": env.str("SQL_DATABASE", DEFAULT_DB_NAME),
        "HOST": env.str("SQL_HOST", ""),
        "PORT": env.str("SQL_PORT", ""),
    }
}

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_PAGE_SIZE = 100

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": env.int("DJANGO_PAGE_SIZE", DEFAULT_PAGE_SIZE),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Weather API",
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
