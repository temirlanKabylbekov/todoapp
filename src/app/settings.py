import os

import environ

root = environ.Path(__file__) - 3        # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env()                   # reading .env file

DEBUG = env('DEBUG')
CI = env('CI', cast=bool, default=False)

SECRET_KEY = env('SECRET_KEY')

SITE_ROOT = root()

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')
STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')
public_root = root.path('public/')

USE_L10N = True
USE_i18N = True
USE_TZ = True
FORMAT_MODULE_PATH = [
    'app.formats',
]
TIME_ZONE = env('TIME_ZONE')
LANGUAGE_CODE = env('LANGUAGE_CODE')
LOCALE_PATHS = ['locale']

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'localhost:8080',
]
ABSOLUTE_HOST = env('ABSOLUTE_HOST')
INTERNAL_IPS = [
    '127.0.0.1',
    '::1',
]

DATABASES = {
    'default': env.db_url(),
}
CONN_MAX_AGE = 300

CACHES = {
    'default': env.cache_url(),
}

TEST_RUNNER = 'app.test.disable_test_command_runner.DisableTestCommandRunner'

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'


def get_git_revision():
    try:
        f = open(os.path.join(env('STATIC_ROOT'), 'revision.txt'))
        return f.readline().strip()
    except BaseException:
        return 'dev'


VERSION = get_git_revision()

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

if not DEBUG:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',

    'django_filters',

    'suit',
    'django.contrib.admin',
    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
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
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'app.renderers.AppJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 24,
    'TIME_FORMAT': '%H:%M',
}

CELERY_ALWAYS_EAGER = env('CELERY_ALWAYS_EAGER', cast=bool, default=DEBUG)  # by default in debug mode we run all celery tasks in foregroud.
CELERY_TIMEZONE = env('TIME_ZONE')
CELERY_ENABLE_UTC = False
CELERY_BROKER_URL = env('CELERY_BACKEND')
CELERY_RESULT_BACKEND = env('CELERY_BACKEND')
