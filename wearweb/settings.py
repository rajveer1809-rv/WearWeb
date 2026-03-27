from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = 'django-insecure-q63vb%o5w6qlx0$o)%kgg5bfybt9d75404y0$&gmb7*lul^um$'
DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com'
]

# ========================
# LOGGING
# ========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

import logging
logger = logging.getLogger(__name__)
logger.info("Settings loaded and logging initialized.")

# ========================
# APPLICATIONS
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cart',
    'core',
    'products',
    'orders',
    'dashboard',
]

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================
# URLS
# ========================
ROOT_URLCONF = 'wearweb.urls'

# ========================
# TEMPLATES
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ========================
# WSGI
# ========================
WSGI_APPLICATION = 'wearweb.wsgi.application'

# ========================
# DATABASE (CORRECT FOR RENDER)
# ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wearweb',
        'USER': 'postgres',
        'PASSWORD': 'rv18',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# In production on Render, we use dj_database_url to parse the database connection string
if os.environ.get("RENDER") or os.environ.get("DATABASE_URL"):
    db_from_env = dj_database_url.config(
        default=os.environ.get("DATABASE_URL", "postgresql://wearweb_user:jO2imasqDffZlwS3jGCuFIBLrxnQ2Pfa@dpg-d70j3ip5pdvs7398m4l0-a/wearweb"),
        conn_max_age=500
    )
    if db_from_env:
        DATABASES['default'] = db_from_env
        logger.info(f"Database configured from environment: {DATABASES['default'].get('HOST')}")
    else:
        logger.warning("DATABASE_URL was set but dj_database_url returned empty config.")

# ========================
# PASSWORD VALIDATION
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# INTERNATIONALIZATION
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC FILES
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========================
# MEDIA FILES
# ========================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ========================
# CUSTOM USER MODEL
# ========================
AUTH_USER_MODEL = 'core.User'

# ========================
# LOGIN REDIRECTS
# ========================
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ========================
# DEFAULT AUTO FIELD
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'