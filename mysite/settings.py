from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


SECRET_KEY = 'django-insecure-+)4$zk*loc4vu0e&exl1mt9mv!vsywof2g&+@dy(^ay%3(8_7x'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vulnerable_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

STATIC_URL = '/static/'

LOGIN_URL = '/login/' 

CSRF_COOKIE_SECURE = True


STATICFILES_DIRS = [
    BASE_DIR / "static",  # For example, a custom static directory in your project
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Add global templates directory if needed
            BASE_DIR / 'vulnerable_app' / 'templates',  # Add the templates for the vulnerable_app
        ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 3. Security Misconfiguration - Debug mode enabled (vulnerable version)
# SECURITY WARNING: don't run with debug turned on in production!
# Vulnerable version, debug should be False in production
# DEBUG = False  # Fix: Debug mode should be off in production for security reasons

DEBUG = os.getenv('DEBUG', 'False') == 'True'  
DEBUG = True

# 4. Identification and Authentication Failures - Weak password policy (vulnerable version)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        #'OPTIONS': {
            #'min_length': 12,  # Fix: Increase minimum length to 12 characters
        #},
    },
    #{
    #    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #},
    #{
    #    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    #},
]

