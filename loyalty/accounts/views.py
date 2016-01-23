from django.contrib import messages
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.views.generic import FormView, ListView, DeleteView
from django.views.generic.base import View
from django.views.generic.edit import BaseFormView
from django.core.urlresolvers import reverse_lazy, reverse

from loyalty import mondo

from .forms import LoginReceiveForm, LinkSchemeForm, OAUTH_STATE_KEY
from .utils import refresh_accounts
from .models import LoyaltySchemeLink


class LoginRedirect(View):
    def get(self, request):
        state = get_random_string()
        request.session[OAUTH_STATE_KEY] = state

        redirect_uri = reverse('accounts:login-receive')

        return redirect(mondo.auth_redirect(state, redirect_uri))


class LoginReceive(BaseFormView):
    form_class = LoginReceiveForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = self.post

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs.update({
            'request': self.request,
            'data': self.request.GET,
        })

        return kwargs

    def form_invalid(self, form):
        errors = [z for x, y in form.errors.items() for z in y]
        for error in errors:
            messages.error(self.request, error)
        return redirect('home:view')

    def form_valid(self, form):
        form.save(self.request)
        return redirect('accounts:dashboard')


class Dashboard(ListView):
    template_name = 'accounts/dashboard.html'
    context_object_name = 'schemes'

    def get_queryset(self):
        return LoyaltySchemeLink.objects.filter(
            account__user=self.request.user,
        )


class LinkScheme(FormView):
    form_class = LinkSchemeForm
    template_name = 'accounts/link.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get(self, *args, **kwargs):
        refresh_accounts(self.request.user)
        return super().get(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteScheme(DeleteView):
    model = LoyaltySchemeLink
    success_url = reverse_lazy('accounts:dashboard')
    template_name = 'accounts/unlink.html'
    context_object_name = 'scheme'
