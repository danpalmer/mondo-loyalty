from django_enumfield import EnumField

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from loyalty.core.fields import OneToOneField
from loyalty.schemes.enums import SchemeEnum


class MondoUser(models.Model):
    user = OneToOneField(User, related_name='mondo_user')

    mondo_user_id = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=512, unique=True)
    access_expires = models.DateTimeField()
    refresh_token = models.CharField(max_length=512, unique=True)


class Account(models.Model):
    user = models.ForeignKey(User, related_name='accounts')
    description = models.CharField(max_length=100)
    webhook_id = models.CharField(max_length=50, unique=True)
    mondo_account_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.description


class LoyaltySchemeLink(models.Model):
    account = models.ForeignKey(Account, related_name='schemes')
    scheme = EnumField(SchemeEnum)
    data = JSONField()
    balance = models.IntegerField(default=0)
    erroring = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('account', 'scheme'),
        )

    def balance_for_display(self):
        if not self.balance:
            return "Use your %s account to see your balance" % (
                self.scheme.display
            )

        return self.scheme.format_balance(self.balance)


class NotifiedTransaction(models.Model):
    """
    We don't record all transactions, only those we act on, so that we can
    ensure we only add a single feed item per transaction
    """
    scheme = models.ForeignKey(
        LoyaltySchemeLink,
        related_name='notified_transactions',
    )

    mondo_transaction_id = models.CharField(max_length=50)
