from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,sbschema,public'
        },
        'TEST': {
            'NAME': 'test_sunneberg',
            'options': '-c search_path=django,public'
        },
        'USER': 'postgres',
        'NAME': 'sunneberg',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}