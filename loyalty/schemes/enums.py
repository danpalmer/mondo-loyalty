import importlib

from django_enumfield import Enum, Item

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage


SchemeEnum = Enum('SchemeEnum')


class Scheme(Item):
    __enum__ = SchemeEnum

    merchant_groups = ()

    username_field = "Username"
    password_field = "Password"

    def get_fields(self):
        return {}

    @property
    def scraper(self):
        try:
            path = 'loyalty.schemes.%s' % self.slug.lower()
            module = importlib.import_module(path)
            return module.Scraper
        except (ImportError, AttributeError):
            return None

    def format_balance(self, balance):
        return '%d points' % balance

    def logo_url(self):
        return '%s%s' % (
            settings.SITE_URL,
            staticfiles_storage.url(
                'images/schemes/%s.png' % self.slug.lower(),
            ),
        )

    def clean_username(self, username):
        return username

    def clean_password(self, password):
        return password


class Nectar(Scheme):
    value = 10

    merchant_groups = ('grp_00008yEduhfVOeBqWmiM2D',)

    username_field = "Nectar Card Number"

    def clean_username(self, username):
        return username.replace('98263000', '').replace(' ', '').strip()


class Sparks(Scheme):
    value = 20

    merchant_groups = ('grp_0000924op0PDw67DG8jJ3Z',)

    username_field = "Email Address"
