web: newrelic-admin run-program gunicorn prolifiko.wsgi --log-file=-
worker: newrelic-admin run-program ./manage.py celery worker -l info
scheduler: ./manage.py celery beat
