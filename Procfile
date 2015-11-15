web: gunicorn loyalty.wsgi --log-file -
worker: celery --app=loyalty worker -l info
