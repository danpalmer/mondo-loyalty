import re
import requests

from lxml import html

from .scrapers import BaseScraper, InvalidCredentialsException

LOGIN_URL = (
    'https://www.marksandspencer.com/webapp/wcs/stores/servlet/'
    'MSSparksLandingPage'
)
LOGIN_ENDPOINT = (
    'https://www.marksandspencer.com/MSLogon?langId=-24&storeId=10151'
)
AUTH_TOKEN_ENDPOINT = (
    'https://www.marksandspencer.com/webapp/wcs/stores/servlet/MSAuthToken'
)
OFFERS_API = (
    'https://api.loyalty.marksandspencer.services/loyalty-service/api/offers'
)
RE_POINTS = re.compile(r'(?P<points>\d+)')


class Scraper(BaseScraper):
    def scrape_balance(username, password):
        session = requests.Session()

        login_response = session.get(LOGIN_URL)

        login_page = html.document_fromstring(login_response.content)
        login_page.make_links_absolute(LOGIN_URL)

        login_form_data = {
            'catalogId': '10051',
            'reLogonURL': 'MSSparksLandingPage',
            'myAcctMain': '',
            'fromOrderId': '*',
            'toOrderId': '.',
            'deleteIfEmpty': '*',
            'continue': '1',
            'createIfEmpty': '1',
            'calculationUsageId': '-1',
            'updatePrices': '0',
            'errorViewName': 'MSSparksLandingPage',
            'forgotPasswordURL': 'MSSparksLandingPage',
            'previousPage': 'logon',
            'rememberMe': 'true',
            'resetConfirmationViewName': 'ResetPasswordForm',
            'URL': '/MSNorth',
            'logonId': username,
            'logonPassword': password,
        }

        logged_in_response = session.post(
            LOGIN_ENDPOINT,
            data=login_form_data,
        )

        # Populate the auth token cookie for the API
        session.get(AUTH_TOKEN_ENDPOINT)

        auth_token = None
        for cookie, value in session.cookies.items():
            if cookie.startswith('MS_AUTH_TOKEN_'):
                auth_token = value

        if not auth_token:
            raise InvalidCredentialsException()

        logged_in_page = html.document_fromstring(logged_in_response.content)
        if logged_in_page.cssselect('form.login-form'):
            raise InvalidCredentialsException()

        offers_response = session.get(OFFERS_API, headers={
            'Authorization': 'MNSAuthToken %s' % auth_token,
        })

        offers = offers_response.json()
        return int(offers['sparks'])
