import datetime

from django import forms
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse

from loyalty import mondo
from loyalty.schemes.enums import SchemeEnum

from .models import MondoUser, Account


OAUTH_STATE_KEY = 'OAUTH_STATE_KEY'


class LoginReceiveForm(forms.Form):
    code = forms.CharField(max_length=500)
    state = forms.CharField(max_length=100)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_state(self):
        state = self.cleaned_data['state']
        session_state = self.request.session.get(OAUTH_STATE_KEY)

        if not session_state:
            raise forms.ValidationError("Unexpected OAuth request received")

        if state != session_state:
            raise forms.ValidationError(
                "OAuth state does not match the expected state",
            )

        return state

    def clean(self):
        self.cleaned_data['auth'] = mondo.exchange_code_for_token(
            self.cleaned_data['code'],
            reverse('accounts:login-receive'),
        )

        return self.cleaned_data

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
