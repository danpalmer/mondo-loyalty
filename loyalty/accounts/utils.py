from django.db.transaction import on_commit

from loyalty import mondo

from .tasks import install_webhook

def refresh_accounts(user):
    accounts = mondo.get_accounts(user)
    for account in accounts['accounts']:
        account, _ = user.accounts.update_or_create(
            mondo_account_id=account['id'],
            defaults={
                'description': account['description'],
            },
        )

        if not account.webhook_id:
            on_commit(lambda: install_webhook(account))
