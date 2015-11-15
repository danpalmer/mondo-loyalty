from django.conf import settings
from django.core.urlresolvers import reverse

from loyalty import mondo
from loyalty.celery import queue

from .models import Account


def install_webhook(account):
    install_webhook_task.delay(account.pk)


@queue.task
def install_webhook_task(account_id):
    account = Account.objects.get(pk=account_id)

    url = '%s%s' % (
        settings.SITE_URL,
        reverse('webhooks:hook', args=(account.pk,)),
    )

    response = mondo.install_webhook(
        account.user,
        account.mondo_account_id,
        url,
    )

    print('Installed hook %s to account %d' % (url, account.pk))

    account.webhook_id = response['webhook']['id']
    account.save()
