# Django settings for checkin project.

# For more information on this file, see
# https://docs.djangoproject.com/en/1.6/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.6/ref/settings/

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django.conf.global_settings as DEFAULT_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

# Private settings
if ON_OPENSHIFT:
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
    DB_PASSWORD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
    DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
else:
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']


SECRET_RECAPTCHA_KEY = os.getenv('SECRET_RECAPTCHA_KEY', '')

# Mandrill (https://mandrillapp.com/) is used to email checkin confirmations
MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']

# MapQuest
MAPQUEST_API_KEY = os.environ['MAPQUEST_API_KEY']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = bool(os.environ.get('DEBUG', False))
    if DEBUG:
        print('WARNING: The DEBUG environment is set to True.')
else:
     DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
     ALLOWED_HOSTS = []
else:
     ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'south',

    # Project apps
    'survey',
    'leaderboard',
    'retail',
    'register'
)

if not ON_OPENSHIFT:
    INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'checkin.urls'

WSGI_APPLICATION = 'checkin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi', 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media files (user uploads, etc.)
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'wsgi', 'media')

# Templates
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)
