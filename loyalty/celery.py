import os

from celery import Celery
from raven import Client
from raven.contrib.celery import register_signal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loyalty.settings')

from django.conf import settings  # noqa


queue = Celery('loyalty')
queue.config_from_object(settings)
queue.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if hasattr(settings, 'RAVEN_CONFIG'):
    # Celery signal registration
    client = Client(dsn=settings.RAVEN_CONFIG['dsn'])
    register_signal(client)


@queue.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
