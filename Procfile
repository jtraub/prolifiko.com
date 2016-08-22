web: gunicorn prolifiko.wsgi --log-file=- --timeout 120
worker: celery -A prolifiko worker -l info -B
