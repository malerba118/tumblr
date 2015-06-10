import os
from tumblr.settings.common import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tumblr4',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "static", "static-only")
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static"),
)