import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yg&*j570!2wgzwae1-n^!nx1ivg*h3&3i-cb2fqm$9g!ji!!o9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'boon.fontoberta.com', 'boon-service', 'taktaan-service']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'oauth2_provider',
    'content',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'boon.urls'

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

WSGI_APPLICATION = 'boon.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Postgres settings

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ['BOON_DB_NAME'],
#         'USER': os.environ['BOON_DB_USER'],
#         'PASSWORD': os.environ['BOON_DB_PASSWORD'],
#         'HOST': os.environ['BOON_DB_HOST'],
#         'PORT': os.environ['BOON_DB_PORT'],
#         'TEST': {
#             'NAME': 'test_' + os.environ['BOON_DB_NAME'],
#         },
#     }
# }

# Sqlite settings

# DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': os.path.join(BASE_DIR, 'boon.db'),
#                 'TEST': {
#                     'NAME': 'test_' + os.environ['BOON_DB_NAME'],
#                 },
#             }
#         }

# MySQL settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['BOON_DB_NAME'],
        'USER': os.environ['BOON_DB_USER'],
        'PASSWORD': os.environ['BOON_DB_PASSWORD'],
        'HOST': os.environ['BOON_DB_HOST'],
        'PORT': os.environ['BOON_DB_PORT'],
        'TEST': {
            'NAME': 'test_' + os.environ['BOON_DB_NAME'],
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',# pylint: disable-msg=line-too-long
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',# pylint: disable-msg=line-too-long
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',# pylint: disable-msg=line-too-long
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',# pylint: disable-msg=line-too-long
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
