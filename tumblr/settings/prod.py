from tumblr.settings.common import *

DEBUG = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tumblr',
		'USER' : 'malerba118',
		'PASSWORD' : 'Rowber118',
        'HOST' : 'tumblr.c3spk20myn8l.us-west-2.rds.amazonaws.com',
        'PORT' : '5432',
    }
}

INSTALLED_APPS += ('storages',)

AWS_STORAGE_BUCKET_NAME = "tumblr-bucket"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL