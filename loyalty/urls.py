from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('loyalty.home.urls', namespace='home')),
    url(r'^account/', include('loyalty.accounts.urls', namespace='accounts')),
    url(r'^webhook/', include('loyalty.webhooks.urls', namespace='webhooks')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
