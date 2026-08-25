from pathlib import Path
from datetime import timedelta
import os

import environ

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# Environment
ENV = env("ENV", default="development").lower()

# Security
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

if ENV == "production":
    DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Custom environment variables
RECAPTCHA_SECRET_KEY = env("RECAPTCHA_SECRET_KEY", default="")

# Production security
if ENV == "production":
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = True

# Installed apps
INSTALLED_APPS = [
    "unfold",
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",
    "django_cleanup.apps.CleanupConfig",
    "django_filters",

    # Project apps
    "accounts",
    "common",
    "products",
    "productMetrics",
    "presence",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL configuration
ROOT_URLCONF = "config.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "config.wsgi.application"

# ASGI application
ASGI_APPLICATION = "config.asgi.application"

# Logging
os.makedirs(BASE_DIR / "logs", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/app.log",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "ERROR",
    },
}

# Cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "default-cache",
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env(
            "REDIS_CACHE_URL",
            default="redis://127.0.0.1:6379/1",
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Database
DATABASES = {
    "default": env.db(),
}

# Password validation
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

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "accounts.authentication.VersionedJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),

    # Throttling settings
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/minute",
        "user": "500/minute",
    },
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int(
            "ACCESS_TOKEN_LIFETIME_MINUTES",
            default=30,
        ),
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env.int(
            "REFRESH_TOKEN_LIFETIME_DAYS",
            default=1,
        ),
    ),

    "ROTATE_REFRESH_TOKENS": env.bool(
        "ROTATE_REFRESH_TOKENS",
        default=False,
    ),

    "BLACKLIST_AFTER_ROTATION": env.bool(
        "BLACKLIST_AFTER_ROTATION",
        default=False,
    ),

    "AUTH_HEADER_TYPES": (
        env.str(
            "AUTH_HEADER_TYPES",
            default="Bearer",
        ),
    ),
}


# Language
LANGUAGE_CODE = "en-us"

# Time zone
TIME_ZONE = "UTC"

# Internationalization
USE_I18N = True

# Time zone support
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Static file storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# CSRF
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Redis database 0 used as the Celery message broker
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://localhost:6379/0")

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
AUTH_USER_MODEL = "accounts.User"

# Clerk Provider
CLERK_SECRET_KEY = env.str("CLERK_SECRET_KEY")
CLERK_AUTHORIZED_PARTIES = env.list("CLERK_AUTHORIZED_PARTIES", default=[])

# Google Provider
GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = env.list("GOOGLE_REDIRECT_URI")

# Facebook Provider
FACEBOOK_APP_ID = env.str("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = env.str("FACEBOOK_APP_SECRET")
FACEBOOK_REDIRECT_URI = env.list("FACEBOOK_REDIRECT_URI")

FACEBOOK_GRAPH_API_VERSION = env.str(
    "FACEBOOK_GRAPH_API_VERSION",
    default="v23.0",
)