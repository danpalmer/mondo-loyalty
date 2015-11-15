from django.views.generic import FormView, ListView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .forms import LoginForm, LinkSchemeForm
from .utils import refresh_accounts
from .models import LoyaltySchemeLink


class Login(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)


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
