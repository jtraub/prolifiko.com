# -*- coding: utf-8 -*-

import os
from datetime import timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

BASE_URL = 'https://app.prolifiko.com'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MAINTENANCE_MODE = 'MAINTENANCE_MODE' in os.environ

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'app',
    'metrics',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'app.middleware.maintenance_middleware',
]

ROOT_URLCONF = 'prolifiko.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.base_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'prolifiko.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.' +
#                 'UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.' +
#                 'MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.' +
#                 'CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.' +
#                 'NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BASE_DIR, 'dist'),
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(levelname)s] %(name)s ' +
                       '%(message)s'),
            # 'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'prolifiko': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        # 'celery.task': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # }
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'Bec and Chris <towritetrack@gmail.com>'

EMAIL_META = {
    'n1_registration': {
        'subject': 'Your 5 day writing challenge – welcome!',
    },
    'n2_new_goal': {
        'subject': '1st goal set + important information',
    },
    'n3_step_1_complete': {
        'subject': 'You’ve completed the toughest step – well done!',
    },
    'n4_step_2_complete': {
        'subject': 'Step 2 done - don\'t stop now',
    },
    'n5_step_3_complete': {
        'subject': 'Step 3 done - 2 steps remain',
    },
    'n6_step_4_complete': {
        'subject': 'Step 4 done - just 1 step to go',
    },
    'n7_goal_complete': {
        'subject': 'Way to go! You’ve finished the challenge',
    },
    'dr1': {
        'subject': 'Yikes! Did you forget to start the writing challenge?',
    },
    'dr2': {
        'subject': 'Writing challenge - get started now!',
    },
    'dr3': {
        'subject': 'Writing challenge - come back anytime',
    },
    'd1': {
        'subject': 'You’ve lost your 1st writing life',
    },
    'd2': {
        'subject': '2nd writing life lost - don’t lose another!',
    },
    'd3': {
        'subject': 'Writing challenge - try again',
    },
    'new_custom_goal': {
        'subject': 'Well done - you\'re on your way',
    },
}

EMAIL_SEND_PERIOD = int(os.environ.setdefault('PF_EMAIL_SEND_PERIOD', '15'))
EMAIL_SEND_PERIOD_UNIT = os.environ.setdefault(
    'PF_EMAIL_SEND_PERIOD_UNIT', 'minutes')
EMAIL_SEND_SCHEDULE = timedelta(**{EMAIL_SEND_PERIOD_UNIT: EMAIL_SEND_PERIOD})

BROKER_URL = os.environ.setdefault('BROKER_URL', 'memory')

CELERYBEAT_SCHEDULE = {
    'send-dr-emails': {
        'task': 'app.tasks.send_dr_emails',
        'schedule': EMAIL_SEND_SCHEDULE,
    },
    'send-d-emails': {
        'task': 'app.tasks.send_d_emails_at_midnight',
        'schedule': EMAIL_SEND_SCHEDULE,
    },
}

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

TEST_EMAIL_ADDRESSES = [
    'mike@mbfisher.com',
    'towritetrack@gmail.com',
    'beccyevans@yahoo.co.uk',
    'revans@emeraldinsight.com',
    'airelembsay@hotmail.co.uk',
    'sally.jenkinson@gmail.com',
    'beprolifiko@gmail.com',
]

TEST_EMAIL_DOMAINS = [
    '@test.com',
    '@t.com',
    '@swarmcommunications.co.uk',
    '@prolifiko.com',
]

CONTINUE_USERS = [
    'continue@test.com',
    'beprolifiko@gmail.com',
]
