web: gunicorn prolifiko.wsgi --log-file=-
worker: ./manage.py celery worker -l info
scheduler: ./manage.py celery beat
