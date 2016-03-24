import dj_database_url


from .base import *


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

try:
    from .local import *
except ImportError:
    pass
