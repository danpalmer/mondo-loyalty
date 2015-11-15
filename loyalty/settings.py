import os

DEBUG = 'PRODUCTION' not in os.environ

if DEBUG:
    from .settings_local import *
else:
    from .settings_prod import *

if not SECRET_KEY:
    raise ValueError("Refusing to start without a secret key")
