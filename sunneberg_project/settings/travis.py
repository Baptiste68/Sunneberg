from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,fooddb,testfooddb'
        },
        'TEST': {
            'NAME': 'test_fooddb',
            'options': '-c search_path=django,testfooddb'
        },
        'USER': 'postgres',
        'NAME': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}