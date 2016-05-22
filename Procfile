web: gunicorn prolifiko.wsgi --log-file=-
worker: celery -A prolifiko worker -l info
scheduler: celery -A prolifiko beat
