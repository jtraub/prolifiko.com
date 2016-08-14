import dj_database_url
from urllib.parse import urlparse

from .base import *


DEBUG = False

BASE_URL = 'https://app.write-track.co'

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [urlparse(BASE_URL).hostname]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

os.environ.setdefault('KEEN_WRITE_KEY', '6d909c8dcad7466b173eb1e1114333455ba' +
                      'af9d2ea61db1bd391d407bd0467bc129f8e7b6449a102f27c12bd' +
                      '09be2ae982abfcc33aa7523bfb3a3f4943db07b701580e933052d' +
                      '9408a1268842b95379fcc0c851bd67552ec74e0e1b3ab55c1a8')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
