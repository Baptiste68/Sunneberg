"""
Django settings for sunneberg_project project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'di!hq)&_99^=$11)objl@!9yn(rr=s@\
    jyqepc_0g32#@=o8qo4') # development key for the moment

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True


if os.environ.get('ENV') == 'PRODUCTION':
    
    # Static files settings
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )

ALLOWED_HOSTS = ['sunnenberg.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'sunneberg.apps.SunnebergConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sunneberg_project.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'sunneberg_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

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
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


if os.environ.get('ENV') == 'PRODUCTION':
        # ...
        # Simplified static file serving.
        # https://warehouse.python.org/project/whitenoise/
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

"""
MEDIA_URL = '/sunneberg/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'sunneberg/media')
"""

MEDIA_URL = '/sunneberg/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'sunneberg/media')

FARM = "Farm_banner_img"
FARM_TXT = "Farm_banner_txt"

COWS = "Cows_banner_img"
COWS_TXT = "Cows_banner_txt"
COWS_VIGNETTE = "Cows_vignette_img"

APPLE = "Apple_banner_img"
APPLE_TXT = "Apple_banner_txt"
APPLE_VIGNETTE = "Apple_vignette_img"

GRAPPES = "Grappes_banner_img"
GRAPPES_TXT = "Grappes_banner_txt"
GRAPPES_VIGNETTE = "Grappes_vignette_img"

MEAT_LIST_NAME = "meat"

NEWSLETTER_USER_LIST = "newslist"

MVP_NEWS = "mvp_news"
NEWS_LIST_FIRST = "first_in_news_list"
NEWS_LIST_SECOND = "second_in_news_list"
NEWS_LIST_THIRD = "third_in_news_list"
NEWS_LIST_FOURTH = "fourth_in_news_list"

# Activate Django-Heroku.
django_heroku.settings(locals())

#Temporar
X_FRAME_OPTIONS = 'SAMEORIGIN'