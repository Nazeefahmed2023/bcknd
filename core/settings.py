"""
Django settings for core project.

Adapted to run apps at project root (no `apps/` package), Channels, Celery, Redis,
Elasticsearch, Kafka and a production-friendly configuration using environment variables.
"""

from datetime import timedelta
import os
from pathlib import Path

# BASE_DIR: backend/
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL = 'users.User'
# -----------------------------------------------------------------------------
# Basic security / environment settings
# -----------------------------------------------------------------------------
# Use environment variables in production. Default values are safe for local dev.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-xiu*kyudvqe^wm$80%^k=a8p7xqa6y7m8srsj7ya^mi!t)dq0w')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# -----------------------------------------------------------------------------
# Application definition
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_elasticsearch_dsl',   # optional, set ES env vars if used
    'channels',

    # Project apps (located at backend/<appname>/)
    'users',
    'catalog',
    'cart',
    'orders',
    'payments',
    'search',
    'delivery',
    'notifications',
    'monitoring',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # If using whitenoise for static files in production, add it here:
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # must be high in the stack
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# Templates - keep as-is; add DIRS if you have project-level templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.environ.get('DJANGO_TEMPLATES_DIR', '')] if os.environ.get('DJANGO_TEMPLATES_DIR') else [],
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

# WSGI (for non-ASGI)
WSGI_APPLICATION = 'core.wsgi.application'
# ASGI (for Channels / WebSockets)
ASGI_APPLICATION = 'core.asgi.application'

# -----------------------------------------------------------------------------
# Database configuration
# -----------------------------------------------------------------------------
# Prefer Postgres in production (set DB env vars). Fall back to sqlite for dev.
if os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -----------------------------------------------------------------------------
# Cache (Redis) - used for OTP, sessions (optional), channel layer, celery broker
# -----------------------------------------------------------------------------
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = os.environ.get('REDIS_DB', '0')
REDIS_URL = os.environ.get('REDIS_URL', f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient',},
    }
}

# -----------------------------------------------------------------------------
# Channels (WebSockets) config - using Redis as channel layer
# -----------------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# -----------------------------------------------------------------------------
# Celery config - broker + results
# -----------------------------------------------------------------------------
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = os.environ.get('DJANGO_TIMEZONE', 'UTC')

# -----------------------------------------------------------------------------
# Elasticsearch (optional) - used by django-elasticsearch-dsl
# -----------------------------------------------------------------------------
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.environ.get('ELASTICSEARCH_HOST', 'elasticsearch:9200'),
    },
}

# -----------------------------------------------------------------------------
# Kafka (optional) - producer/consumer bootstrap servers
# # -----------------------------------------------------------------------------
# KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]


# -----------------------------------------------------------------------------
# Password validators (unchanged)
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE', 'en-us')
TIME_ZONE = os.environ.get('DJANGO_TIMEZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static & media files
# -----------------------------------------------------------------------------
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.environ.get('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', str(BASE_DIR / 'media'))

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# REST Framework + JWT
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.environ.get('DJANGO_PAGE_SIZE', 20)),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_DAYS', 7))),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------
if os.environ.get('CORS_ALLOWED_ORIGINS'):
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(",")
else:
    # allow all during local development if DEBUG
    CORS_ALLOWED_ORIGINS = []
    if DEBUG:
        CORS_ALLOW_ALL_ORIGINS = True

# -----------------------------------------------------------------------------
# Sessions and CSRF (leave default unless you want JWT-only stateless)
# -----------------------------------------------------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# -----------------------------------------------------------------------------
# Logging - reasonable defaults
# -----------------------------------------------------------------------------
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[%(levelname)s] %(asctime)s %(name)s: %(message)s'},
        'simple': {'format': '[%(levelname)s] %(message)s'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'root': {'handlers': ['console'], 'level': LOG_LEVEL},
    'loggers': {
        'django': {'handlers': ['console'], 'level': LOG_LEVEL, 'propagate': False},
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
        # add other loggers for celery, kafka, etc.
    },
}

# -----------------------------------------------------------------------------
# Additional helpful env-driven flags
# -----------------------------------------------------------------------------
# Admins, managers
ADMINS = tuple([tuple(a.split(':')) for a in os.environ.get('DJANGO_ADMINS', '').split(',') if a])
MANAGERS = ADMINS

# -----------------------------------------------------------------------------
# Optional: Email settings (for production configure SMTP)
# -----------------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() in ('1', 'true')

# -----------------------------------------------------------------------------
# Health check / monitoring endpoints (example)
# -----------------------------------------------------------------------------
HEALTH_CHECK_ENABLED = True

# -----------------------------------------------------------------------------
# Print helpful info when running manage.py runserver (dev)
# -----------------------------------------------------------------------------
if DEBUG:
    print("DJANGO DEBUG MODE: ON")
    print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
    print("DATABASES:", {k: v for k, v in DATABASES.items()})

# End of settings.py
