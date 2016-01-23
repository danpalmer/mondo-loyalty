from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import LoginRedirect, LoginReceive, Dashboard, LinkScheme, \
    DeleteScheme

urlpatterns = [
    url(
        r'^login$',
        LoginRedirect.as_view(),
        name='login',
    ),
    url(
        r'^login-receive$',
        LoginReceive.as_view(),
        name='login-receive',
    ),

    # Login Required
    url(
        r'^$',
        login_required(Dashboard.as_view()),
        name='dashboard',
    ),
    url(
        r'^schemes/add$',
        login_required(LinkScheme.as_view()),
        name='link-scheme',
    ),
    url(
        r'^schemes/(?P<pk>\d+)/delete',
        login_required(DeleteScheme.as_view()),
        name='unlink-scheme',
    ),

    url(
        r'^logout$',
        login_required(auth_views.logout),
        {'next_page': reverse_lazy('home:view')},
        name='logout',
    )
]
