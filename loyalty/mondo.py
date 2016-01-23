import datetime
import requests
import strict_rfc3339

from urllib.parse import urlencode

from django.conf import settings


def url(path):
    return '%s%s' % (settings.MONDO_API_BASE, path)


URL_TOKEN = url('oauth2/token')
URL_REFRESH = url('oauth2/token')
URL_WEBHOOK_CREATE = url('webhooks')
URL_ACCOUNTS = url('accounts')
URL_TRANSACTIONS = url('transactions')
URL_TRANSACTION_FMT = url('transaction/%s')
URL_FEED = url('feed')


def auth_redirect(state, redirect_uri):
    args = urlencode({
        'redirect_uri': settings.SITE_URL + redirect_uri,
        'client_id': settings.MONDO_CLIENT_ID,
        'state': state,
        'response_type': 'code',
    })

    return '{uri}?{args}'.format(
        uri=settings.MONDO_AUTH_URI,
        args=args,
    )


def exchange_code_for_token(code, redirect_uri):
    response = requests.post(
        URL_TOKEN,
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.MONDO_CLIENT_ID,
            'client_secret': settings.MONDO_CLIENT_SECRET,
            'redirect_uri': settings.SITE_URL + redirect_uri,
            'code': code,
        }
    )

    return response.json()


def get_accounts(user):
    return requests.get(URL_ACCOUNTS, headers=auth_header(user)).json()


def install_webhook(user, account_id, url):
    webhook_response = requests.post(URL_WEBHOOK_CREATE, data={
        'account_id': account_id,
        'url': url,
    }, headers=auth_header(user))

    return webhook_response.json()


def get_most_recent_transaction(user, account_id):
    last_day = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    transactions_response = requests.get(
        URL_TRANSACTIONS,
        params={
            'account_id': account_id,
            'expand[]': 'merchant',
            'since': strict_rfc3339.timestamp_to_rfc3339_utcoffset(
                last_day.timestamp(),
            ),
        },
        headers=auth_header(user),
    )

    transactions = transactions_response.json()['transactions']

    if not transactions:
        return None

    transactions = sorted(
        transactions,
        key=lambda x: x['created'],
        reverse=True,
    )

    return transactions[0]


def insert_feed_item(user, account_id, feed_item):
    data = {
        'account_id': account_id,
        'type': 'basic',
    }

    for key, value in feed_item.items():
        data['params[%s]' % key] = value

    feed_item_response = requests.post(
        URL_FEED,
        data=data,
        headers=auth_header(user),
    )

    return feed_item_response.json()


# Utils

def auth_payload(data):
    data.update({
        'client_id': settings.MONDO_CLIENT_ID,
        'client_secret': settings.MONDO_CLIENT_SECRET,
    })
    return data

def auth_header(user):
    return {'Authorization': 'Bearer %s' % user.mondo_user.access_token}
