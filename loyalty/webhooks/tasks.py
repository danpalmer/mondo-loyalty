from loyalty import mondo
from loyalty.celery import queue
from loyalty.accounts.models import Account, LoyaltySchemeLink
from loyalty.schemes.enums import SchemeEnum
from loyalty.schemes.scrapers import InvalidCredentialsException

def scrape_balance_for_last_transaction(account):
    scrape_balance_for_last_transaction_task.delay(account.pk)


@queue.task
def scrape_balance_for_last_transaction_task(account_id):
    account = Account.objects.prefetch_related('schemes').get(pk=account_id)

    transaction = mondo.get_most_recent_transaction(
        account.user,
        account.mondo_account_id,
    )

    for scheme in SchemeEnum:
        if transaction['merchant']['group_id'] not in scheme.merchant_groups:
            continue

        account_scheme = account.schemes.filter(
            scheme=scheme.value,
            erroring=False,
        ).get()

        try:
            new_balance = scheme.scraper.scrape_balance(**account_scheme.data)
            if not new_balance:
                continue
        except InvalidCredentialsException:
            account_scheme.erroring = True
            account_scheme.save()
            return

        account_scheme.balance = new_balance
        account_scheme.save()

        insert_new_balance.delay(account_scheme.pk, transaction['id'])
        return


@queue.task
def insert_new_balance(scheme_id, mondo_transaction_id):
    scheme = LoyaltySchemeLink.objects.select_related(
        'account__user',
    ).get(
        pk=scheme_id,
    )

    notified_transaction, created = scheme.notified_transactions.get_or_create(
        mondo_transaction_id=mondo_transaction_id,
    )

    if not created:
        return

    mondo.insert_feed_item(
        scheme.account.user,
        scheme.account.mondo_account_id,
        {
            'title': "Your %s balance is %d" % (
                scheme.scheme.display,
                scheme.balance,
            ),
            'image_url': scheme.scheme.logo_url(),
        },
    )
