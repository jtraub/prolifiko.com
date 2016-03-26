from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+t!o-)1p_j+#03=(nx(xn(d)3a-h+pup_2%m6^cku3o!856iex'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

os.environ.setdefault('KEEN_PROJECT_ID', '56f65f4446f9a7095a7b604b')
os.environ.setdefault('KEEN_WRITE_KEY', '6d909c8dcad7466b173eb1e1114333455ba' +
                      'af9d2ea61db1bd391d407bd0467bc129f8e7b6449a102f27c12bd' +
                      '09be2ae982abfcc33aa7523bfb3a3f4943db07b701580e933052d' +
                      '9408a1268842b95379fcc0c851bd67552ec74e0e1b3ab55c1a8')


try:
    from .local import *
except ImportError:
    pass
