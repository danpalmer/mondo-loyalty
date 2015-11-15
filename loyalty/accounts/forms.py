import datetime

from django import forms
from django.utils import timezone
from django.contrib.auth import login, authenticate

from loyalty import mondo
from loyalty.schemes.enums import SchemeEnum

from .models import MondoUser, Account


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        response = mondo.login(username, password)

        self.cleaned_data['auth'] = response

    def save(self, request):
        user_id = self.cleaned_data['auth']['user_id']
        access_token = self.cleaned_data['auth']['access_token']
        refresh_token = self.cleaned_data['auth']['refresh_token']
        expires_in = datetime.timedelta(
            seconds=self.cleaned_data['auth']['expires_in']
        )

        user = authenticate(remote_user=user_id)
        login(request, user)

        if not user.mondo_user:
            user.mondo_user = MondoUser(
                user=user,
                mondo_user_id=user_id,
            )

        user.mondo_user.access_token = access_token
        user.mondo_user.access_expires = timezone.now() + expires_in
        user.mondo_user.refresh_token = refresh_token
        user.mondo_user.save()

        return user


class LinkSchemeForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    scheme = forms.ChoiceField(choices=SchemeEnum.get_choices())

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields['account'].queryset = Account.objects.filter(user=user)

    def clean_scheme(self):
        scheme_value = int(self.cleaned_data['scheme'])
        return SchemeEnum.from_value(scheme_value)

    def save(self):
        account = self.cleaned_data['account']
        scheme = self.cleaned_data['scheme']

        username = scheme.clean_username(self.cleaned_data['username'])
        password = scheme.clean_password(self.cleaned_data['password'])

        account.schemes.create(
            scheme=scheme,
            data={
                'username': username,
                'password': password,
            }
        )
