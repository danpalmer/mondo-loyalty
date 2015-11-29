web: gunicorn loyalty.wsgi --log-file -
worker: celery --without-gossip --without-mingle --without-heartbeat --app=loyalty worker -l info
