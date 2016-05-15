import dj_database_url
from urllib.parse import urlparse

from .base import *


DEBUG = False

BASE_URL = 'http://prolifikoapp.herokuapp.com'

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

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_SERVER_NAME = 'prolifiko.com'
MAILGUN_ACCESS_KEY = 'key-9fa666daad5abd35f2f316177ecb7527'

try:
    from .local import *
except ImportError:
    pass
