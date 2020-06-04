import os
import datetime
from conf import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "info@coronawhy.org"
EMAIL_HOST_PASSWORD = "coronawhy"
EMAIL_PORT = 587

ROOT_URLCONF = 'covidPortalApp.urls'

## Make this unique, and don't share it with anybody.
SECRET_KEY = '7xrw^s(wus37(pbke+k&=8iikd)eipxxwmbm$$^^13n3c_z&%2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'covidPortalApp',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'explorer.apps.ExplorerConfig',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=180000)
}

STATICFILES_STORAGE = "require.storage.OptimizedStaticFilesStorage"

MIDDLEWARE = (
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# allow access to angular
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# table prefix name
DB_PREFIX = 'covidPortalApp'
# Local time zone for this installation. Choices can be found here:

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': COVID_DB_SCHEMA,                      # Or path to database file if using sqlite3.
#         'USER': COVID_DB_USER,                      # Not used with sqlite3.
#         'PASSWORD': COVID_DB_PASSWORD,                  # Not used with sqlite3.
#         'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
#         'OPTIONS': {
#             'init_command': 'SET default_storage_engine=INNODB',
#             }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [
     os.path.join(BASE_DIR, './static'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

MEDIA_URL = ''
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = "/covidPortalApp/"
LOGOUT_REDIRECT_URL = "/covidPortalApp/"
