web: newrelic-admin run-program gunicorn prolifiko.wsgi --log-file=-
worker: newrelic-admin run-program ./manage.py celery worker -B -l info
