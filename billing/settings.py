"""
Django settings for billing project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(a7i-b94@@_j604q3q@yzty$g98&wv)^p2y$#=$5u+a1fmw@xz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'longer_username',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'packages',
    'payments',
    'search',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'billing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'billing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'radius_xwf',
        'USER': 'radius_xwf',
        'PASSWORD': 'radpass',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static_live")

LOGIN_URL = 'accounts:login'

LOGIN_REDIRECT_URL = 'index'

DEFAULT_FROM_EMAIL = 'test@example.com'

SITE_ID = 1

# Email settings
EMAIL_HOST = '74.55.86.74'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'deone'
EMAIL_HOST_PASSWORD = '@dune369'

# VMS
VMS_URL = "http://vms-deone.c9users.io/vouchers/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_INVALIDATE_URL = VMS_URL + "invalidate"

SUCCESS_URL = "http://billing-deone.c9users.io/success/"

# SMS settings - SMSGH
SMS_URL = 'https://api.smsgh.com/v3/messages/send'
SMS_PARAMS = {
    'From': 'XWF',
    'Content': 'Welcome to Spectra WiFi! You may log into your dashboard at xwf.spectrawireless.com. Our customer care line is 055 324 2528.',
    'ClientId': 'qtrufcsm',
    'ClientSecret': 'mgzqaxfe',
    'RegisteredDelivery': 'true'
}

# TWILIO_ACCOUNT_SID = 'ACe0325806bc5842a1f96a115e8c21a384'
# TWILIO_AUTH_TOKEN = '90bd6b99b70d51d97d637a98e33ce8a7'
# TWILIO_NUMBER = '+18177569348'

# More settings

# Speed variants
DELUXE = '2'
SUPREME = '4'

# Speed names
SPEED_NAME_MAP = {
    DELUXE: '2Mbps Deluxe',
    SUPREME: '4Mbps Supreme',
}

SPEED_CHOICES = (
    (DELUXE, SPEED_NAME_MAP[DELUXE]),
    (SUPREME, SPEED_NAME_MAP[SUPREME]),
)

# Volume variants
HUNDRED_MB = '0.1'
THREE_HUNDRED_MB = '0.3'
ONE = '1'
TWO = '2'
TWO_POINT_FIVE = '2.5'
SIX = '6'
TWELVE = '12'
FIFTEEN = '15'

# Volume names
VOLUME_NAME_MAP = {
    HUNDRED_MB: '0.1GB',
    THREE_HUNDRED_MB: '0.3GB',
    ONE: '1GB',
    TWO: '2GB',
    TWO_POINT_FIVE: '2.5GB',
    SIX: '6GB',
    TWELVE: '12GB',
    FIFTEEN: '15GB',
}

VOLUME_CHOICES = (
    (HUNDRED_MB, VOLUME_NAME_MAP[HUNDRED_MB]),
    (THREE_HUNDRED_MB, VOLUME_NAME_MAP[THREE_HUNDRED_MB]),
    (ONE, VOLUME_NAME_MAP[ONE]),
    (TWO, VOLUME_NAME_MAP[TWO]),
    (TWO_POINT_FIVE, VOLUME_NAME_MAP[TWO_POINT_FIVE]),
    (SIX, VOLUME_NAME_MAP[SIX]),
    (TWELVE, VOLUME_NAME_MAP[TWELVE]),
    (FIFTEEN, VOLUME_NAME_MAP[FIFTEEN]),
)

TEST_PERIOD = 'Ten'
DAILY = 'Daily'
WEEKLY = 'Weekly'
MONTHLY = 'Monthly'

PACKAGE_TYPES = (
    (TEST_PERIOD, 'Ten'),
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
)

PACKAGE_TYPES_HOURS_MAP = {
    TEST_PERIOD: 0.17,
    DAILY: 1 * 24,
    WEEKLY: 7 * 24,
    MONTHLY: 30 * 24
}

MAX_FILE_LENGTH = 30

# Set this to False to test BulkUserUploadForm.clean()
# EXCEED_MAX_USER_COUNT = True
EXCEED_MAX_USER_COUNT = False

# Payments
STORE_NAME = 'Spectra Wireless'

PAYMENT_DESCRIPTION = 'Package Purchase'
PAYMENT_MASTER_KEY = 'cef70167-7dec-458e-b5bf-1befb4196565'

# - Test API
PAYMENT_TEST_URL = 'https://app.mpowerpayments.com/sandbox-api/v1/checkout-invoice/create'
PAYMENT_TEST_PRIVATE_KEY = 'test_private_-TBbZrbdchpR6RZ9aB6g9Hx6-wk'

PHONE_NUMBER_PREFIXES = ['020', '023', '024', '026', '027', '028', '050', '052', '054', '055', '056', '057']

PASSWORD_RESET_TIMEOUT_DAYS = 90