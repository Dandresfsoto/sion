from .base import *
from .base import env

DEBUG = False

ALLOWED_HOSTS = ['iracaz1.com','localhost']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT'),
        }
}


# Storages
AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = env('AZURE_CONTAINER')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AZURE_CUSTOM_DOMAIN = env('AZURE_CUSTOM_DOMAIN')
MEDIA_URL = env('MEDIA_URL')