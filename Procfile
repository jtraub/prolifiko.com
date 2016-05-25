web: newrelic-admin run-program gunicorn prolifiko.wsgi --log-file=-
worker: ./manage.py celery worker -B
