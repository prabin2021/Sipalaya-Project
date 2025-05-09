"""
Django settings for Sipalaya_Backend project.

Generated by 'django-admin startproject' using Django 4.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q1ozl!q3mixmdx5@r$^6(1q-h&by8d)65%v0%apnk1ymu(vlb%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "courses",
    "homepage",
    "testimonials",
    "stud_portal",
    "blog",
    "payments",
    "demo_classes",
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

ROOT_URLCONF = "Sipalaya_Backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ 
            BASE_DIR /'templates',
            ],
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

WSGI_APPLICATION = "Sipalaya_Backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

import os
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/protected/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/login/'  # Redirect to login after logout

# Payment Gateway Settings
# Stripe Settings (Commented out for now)
# STRIPE_PUBLIC_KEY = 'pk_test_51NxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# STRIPE_SECRET_KEY = 'sk_test_51NxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# STRIPE_WEBHOOK_SECRET = 'whsec_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Khalti Settings (Commented out for now)
# KHALTI_URL = 'https://a.khalti.com/api/v2/payment/verify/'
# KHALTI_SECRET_KEY = 'test_secret_key'
# KHALTI_PUBLIC_KEY = 'test_public_key'

# eSewa Payment Gateway Configuration Removed
ESEWA_SECRET_KEY = os.getenv('ESEWA_SECRET_KEY', '8gBm/:&EnhH.1/q(')  # Test secret key
ESEWA_BASE_URL = os.getenv('ESEWA_BASE_URL', 'https://uat.esewa.com.np')  # UAT environment
ESEWA_PAYMENT_URL = f'{ESEWA_BASE_URL}/epay/main'
ESEWA_TRANSACTION_STATUS_URL = f'{ESEWA_BASE_URL}/api/epay/transaction/status/v2'
ESEWA_SUCCESS_URL = os.getenv('ESEWA_SUCCESS_URL', 'http://localhost:8000/payments/esewa/success/')
ESEWA_FAILURE_URL = os.getenv('ESEWA_FAILURE_URL', 'http://localhost:8000/payments/esewa/failure/')

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'payments_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'payments.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'payments': {
            'handlers': ['payments_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
# settings.py
ESEWA_CONFIG = {
    'TEST_MODE': True,  # Set to False in production
    'TEST_URL': 'https://rc-epay.esewa.com.np/api/epay/main/v2/form',
    'PRODUCTION_URL': 'https://epay.esewa.com.np/api/epay/main/v2/form',
    'TEST_SECRET_KEY': '8gBm/:&EnhH.1/q(',
    'TEST_PRODUCT_CODE': 'EPAYTEST',
}

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'binodtharu122g@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'npwt odje yaif vblx')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'binodtharu122g@gmail.com')

# Add SITE_ID setting
SITE_ID = 1