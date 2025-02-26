"""
Django settings for beagle project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import ldap
import json
import datetime
from django_auth_ldap.config import LDAPSearch

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4gm1)1&0x71+^vwo)rf=%%b)f3l$%u893bs$scif+h#nj@eyx('

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'prod')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == 'dev'

ALLOWED_HOSTS = os.environ.get('BEAGLE_ALLOWED_HOSTS', 'localhost').split(',')

CORS_ORIGIN_ALLOW_ALL = True


# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'runner.apps.RunnerConfig',
    'beagle_etl.apps.BeagleEtlConfig',
    'file_system.apps.FileSystemConfig',
    'notifier.apps.NotifierConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'rangefilter',
    'rest_framework',
    'corsheaders',
    'drf_multiple_model',
    'drf_yasg'
]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "secret_key",
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}


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

AUTH_LDAP_SERVER_URI = os.environ.get('BEAGLE_AUTH_LDAP_SERVER_URI', "url_goes_here")

AUTH_LDAP_AUTHORIZE_ALL_USERS = True

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_REFERRALS: 0}
AUTH_LDAP_START_TLS = False

AUTH_LDAP_CACHE_TIMEOUT = 0

AUTH_LDAP_USER_DN_TEMPLATE = '%(user)s@mskcc.org'

AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True

AUTH_LDAP_NO_NEW_USERS = True

# AUTH_LDAP_GROUP_TYPE = MemberDNGroupType()
# AUTH_LDAP_GROUP_SEARCH = LDAPSearchUnion(
#     LDAPSearch('DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG', ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"),
# )

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG',
    ldap.SCOPE_SUBTREE,
    '(sAMAccountName=%(user)s)',
    ['sAMAccountName', 'displayName', 'memberOf', 'title']
)

# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#     'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG',
#     ldap.SCOPE_SUBTREE,
#     '(sAMAccountName=%(user)s)',
#     '(objectClass=posixGroup)',)

AUTH_LDAP_ALWAYS_UPDATE_USER = True

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# AUTH_LDAP_USER_ATTR_MAP = {
#     "first_name": "givenName",
#     "last_name": "sn",
#     "email": "mail",
# }

# AUTH_LDAP_FIND_GROUP_PERMS = True

# AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn", "email": "mail"}

# AUTH_LDAP_MIRROR_GROUPS = True

# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_active": "DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG",
#     "is_staff": (
#         LDAPGroupQuery("cn=active,ou=groups,dc=ROOT,dc=com")
#         | LDAPGroupQuery("cn=active,ou=groups,dc=ROOT,dc=com")
#     ),
#     "is_superuser": "cn=active,ou=groups,dc=ROOT,dc=com",
# }

ROOT_URLCONF = 'beagle.urls'

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

WSGI_APPLICATION = 'beagle.wsgi.application'


DB_NAME = os.environ['BEAGLE_DB_NAME']
DB_USERNAME = os.environ['BEAGLE_DB_USERNAME']
DB_PASSWORD = os.environ['BEAGLE_DB_PASSWORD']
DB_HOST = os.environ.get('BEAGLE_DB_URL', 'localhost')
DB_PORT = os.environ.get('BEAGLE_DB_PORT', 5432)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'DISABLE_SERVER_SIDE_CURSORS': True
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

PAGINATION_DEFAULT_PAGE_SIZE = 10

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'beagle.pagination.BeaglePagination',
    'PAGE_SIZE': PAGINATION_DEFAULT_PAGE_SIZE,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}


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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL='/admin/login/'
LOGOUT_URL='/admin/logout/'

SWAGGER_SETTINGS = {
    'VALIDATOR_URL':None
}

RABIX_URL = os.environ.get('BEAGLE_RABIX_URL')
RABIX_PATH = os.environ.get('BEAGLE_RABIX_PATH')

MEMCACHED_PORT = os.environ.get('BEAGLE_MEMCACHED_PORT', 11211)

if ENVIRONMENT == "dev":
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'beagle-cache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
            'LOCATION': '127.0.0.1:%s' % MEMCACHED_PORT,
            'OPTIONS': {# see https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html#pymemcache.client.base.Client
                'default_noreply': False
            }
        }
    }

RABBITMQ_USERNAME = os.environ.get('BEAGLE_RABBITMQ_USERNAME', 'guest')
RABBITMQ_PASSWORD = os.environ.get('BEAGLE_RABBITMQ_PASSWORD', 'guest')
RABBITMQ_URL = os.environ.get('BEAGLE_RABBITMQ_URL', 'localhost')

CELERY_BROKER_URL = 'amqp://%s:%s@%s/' % (RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 1
CELERY_EVENT_QUEUE_PREFIX = os.environ.get('BEAGLE_CELERY_QUEUE_PREFIX', 'beagle.production')

LIMS_USERNAME = os.environ.get('BEAGLE_LIMS_USERNAME')
LIMS_PASSWORD = os.environ.get('BEAGLE_LIMS_PASSWORD')
ETL_USER = os.environ.get('BEAGLE_ETL_USER')

LIMS_URL = os.environ.get('BEAGLE_LIMS_URL', 'https://igolims.mskcc.org:8443')

IMPORT_FILE_GROUP = os.environ.get('BEAGLE_IMPORT_FILE_GROUP', '1a1b29cf-3bc2-4f6c-b376-d4c5d701166a')

POOLED_NORMAL_FILE_GROUP = os.environ.get('BEAGLE_POOLED_NORMAL_FILE_GROUP', 'b6857a56-5d45-451f-b4f6-26148946080f')

DMP_BAM_FILE_GROUP = os.environ.get('BEAGLE_DMP_BAM_FILE_GROUP', '9ace63bf-ed55-461c-9ac0-1c5ee710d957')

RIDGEBACK_URL = os.environ.get('BEAGLE_RIDGEBACK_URL', 'http://localhost:5003')

LOG_PATH = os.environ.get('BEAGLE_LOG_PATH', 'beagle-server.log')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH,
            "maxBytes": 209715200,
            "backupCount": 10
        }
    },
    "loggers": {
        "django_auth_ldap": {
            "level": "DEBUG", "handlers": ["console"]
        },
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

SUPPORTED_NOTIFIERS = ('JIRA', 'NONE')

NOTIFIER_ACTIVE = os.environ.get("BEAGLE_NOTIFIER_ACTIVE", True)

NOTIFIER_CC = os.environ.get("BEAGLE_NOTIFIER_CC", '') # Put "CC [~webbera] and [~socci]" for production
NOTIFIER_STORAGE_DIR = os.environ.get("BEAGLE_NOTIFIER_STORAGE_DIR", '/tmp')
NOTIFIER_FILE_GROUP = os.environ.get("BEAGLE_NOTIFIER_FILE_GROUP")

JIRA_URL = os.environ.get("JIRA_URL", "")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME", "")
JIRA_PASSWORD = os.environ.get("JIRA_PASSWORD", "")
JIRA_PROJECT = os.environ.get("JIRA_PROJECT", "")
JIRA_PIPELINE_FIELD_ID = os.environ.get('JIRA_PIPELINE_FIELD_ID', "customfield_10901")

BEAGLE_URL = os.environ.get('BEAGLE_URL', 'http://silo:5001')

BEAGLE_RUNNER_QUEUE = os.environ.get('BEAGLE_RUNNER_QUEUE', 'beagle_runner_queue')
BEAGLE_DEFAULT_QUEUE = os.environ.get('BEAGLE_DEFAULT_QUEUE', 'beagle_default_queue')
BEAGLE_JOB_SCHEDULER_QUEUE = os.environ.get('BEAGLE_JOB_SCHEDULER_QUEUE', 'beagle_job_scheduler_queue')
BEAGLE_SHARED_TMPDIR = os.environ.get('BEAGLE_SHARED_TMPDIR', '/juno/work/ci/temp')

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
TEST_FIXTURE_DIR = os.path.join(ROOT_DIR, "fixtures", "tests")

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

SAMPLE_ID_METADATA_KEY = 'sampleId'

BEAGLE_NOTIFIER_EMAIL_GROUP = os.environ.get('BEAGLE_NOTIFIER_EMAIL_GROUP', '946a922c-8c6b-4cba-8754-16df02f05d2a')
BEAGLE_NOTIFIER_EMAIL_ABOUT_NEW_USERS = os.environ.get('BEAGLE_NOTIFIER_EMAIL_ABOUT_NEW_USERS')
BEAGLE_NOTIFIER_EMAIL_FROM = os.environ.get('BEAGLE_NOTIFIER_EMAIL_FROM')

PERMISSION_DENIED_CC = json.loads(os.environ.get('BEAGLE_PERMISSION_DENIED_CC', '{}'))
PERMISSION_DENIED_EMAILS = json.loads(os.environ.get('BEAGLE_PERMISSION_DENIED_EMAIL', '{}'))

## Tempo

WES_ASSAYS = os.environ.get('BEAGLE_NOTIFIER_WES_ASSAYS', 'WholeExomeSequencing').split(',')
NOTIFIER_WES_CC = os.environ.get('BEAGLE_NOTIFIER_WHOLE_EXOME_SEQUENCING_CC', '')

DEFAULT_MAPPING = json.loads(os.environ.get("BEAGLE_COPY_MAPPING", "{}"))
