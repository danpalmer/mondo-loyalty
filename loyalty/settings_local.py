import os

from .settings_prod import *

DEBUG = 'PRODUCTION' not in os.environ

SECRET_KEY = '8gCpFpsR7LQ32hI1ewZMiWwzihhY7s8dzfBZ4Jxo'

SITE_URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'NAME': 'loyalty',
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'ATOMIC_REQUESTS': True,
    }
}

INSTALLED_APPS = [
    x for x in INSTALLED_APPS if x not in (
        'raven.contrib.django.raven_compat',
    )
]

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CELERY_ALWAYS_EAGER = DEBUG
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
