from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,sunneberg,testsunneberg'
        },
        'TEST': {
            'NAME': 'test_sunneberg',
            'options': '-c search_path=django,testsunneberg'
        },
        'USER': 'postgres',
        'NAME': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}