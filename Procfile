web: newrelic-admin run-program gunicorn prolifiko.wsgi --log-file=-
worker: newrelic-admin run-program ./manage.py celeryd -E -B --loglevel=INFO
