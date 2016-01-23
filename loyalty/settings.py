import os

PRODUCTION = 'PRODUCTION' in os.environ
DEBUG = 'DEBUG' in os.environ

if PRODUCTION:
    from .settings_prod import *
else:
    from .settings_local import *

if not SECRET_KEY:
    raise ValueError("Refusing to start without a secret key")
