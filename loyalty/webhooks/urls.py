from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import Hook

urlpatterns = [
    url(r'^account/(?P<pk>\d+)$', csrf_exempt(Hook.as_view()), name='hook'),
]
