from django_enumfield.context_processors import get_enums

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': simple_reverse,
        'settings': settings,
        'enums': get_enums(),
        'get_messages': messages.get_messages,
    })
    return env

def simple_reverse(url, *args, **kwargs):
    return reverse(url, args=args, kwargs=kwargs)
