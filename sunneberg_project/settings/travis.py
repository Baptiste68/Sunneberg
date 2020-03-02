from . import *

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'NAME': 'sunneberg',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}