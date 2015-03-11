"""
Django settings for refilm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/',
)
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False
TEMPLATE_DEBUG = False
if os.environ.get("I_AM_IN_DEV_ENV"):
    DEBUG = True
    TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    ".herokuapp.com",
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'video_editing.film',
    # 'workout_generator.access_token',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    # 'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'video_editing.urls'

WSGI_APPLICATION = 'video_editing.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_ROOT = 'staticfiles'

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = "mturk-static"

if os.environ.get("I_AM_IN_DEV_ENV"):
    STATIC_URL = '/static/'
else:
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATIC_URL = "http://s3.amazonaws.com/%s/" % AWS_STORAGE_BUCKET_NAME


ADMIN_EMAILS = (
    'scott.lobdell@gmail.com',
)

if os.environ.get("I_AM_IN_DEV_ENV"):
    HOST_URL = "http://localhost:5000"
else:
    HOST_URL = "http://mturk-demonstration.herokuapp.com"
