"""
Django settings for prolifiko project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

BASE_URL = 'https://prolifiko.com'

DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djcelery',
    'kombu.transport.django',

    'app',
    'home',
    'search',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
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
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "prolifiko"

LOGIN_URL = '/app/login/'
LOGIN_REDIRECT_URL = '/app/'

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
            # 'level': 'DEBUG' if DEBUG else 'INFO'
        }
    }
}

EMAIL_META = {
    'n1_registration': {
        'subject': "Your 5 Day Writing Challenge – Welcome!",
    },
    'n2_new_goal': {
        'subject': "1st Goal Set + Important Information",
    },
    'n3_step_1_complete': {
        'subject': "You’ve Completed the Toughest Step – Well Done!",
    },
    'n4_step_2_complete': {
        'subject': "Step 2 Done: Set Your Next Step",
    },
    'n5_step_3_complete': {
        'subject': "Aced the 3rd Step: Only 2 Steps Remain",
    },
    'n6_step_4_complete': {
        'subject': "4th Step Won: Just 1 More To Go!",
    },
    'n7_goal_complete': {
        'subject': "Way to Go! You’ve Finished the Challenge",
    },
    'dr1': {
        'subject': 'Do You Want to Kickstart Your Writing?',
    },
    'dr2': {
        'subject': 'Writing Challenge: Don’t quit now',
    },
    'dr3': {
        'subject': 'Writing Challenge: Check in Anytime',
    },
}

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERYBEAT_SCHEDULE = {
    'send-dr-emails': {
        'task': 'app.tasks.send_dr_emails',
        'schedule': timedelta(hours=1),
    },
    'send-d-emails': {
        'task': 'app.tasks.send_d_emails',
        'schedule': timedelta(hours=1),
    },
}
