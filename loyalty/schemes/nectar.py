import re
import requests

from lxml import html

from .scrapers import BaseScraper, InvalidCredentialsException

LOGIN_URL = 'https://www.nectar.com/login'
RE_POINTS = re.compile(r'(?P<points>\d+(,\d+)*)')


class Scraper(BaseScraper):
    def scrape_balance(username, password):
        session = requests.Session()

        login_response = session.get(LOGIN_URL)

        login_page = html.document_fromstring(login_response.content)
        login_page.make_links_absolute(LOGIN_URL)

        login_form = login_page.forms[0]
        login_form_data = dict(login_form.form_values())
        login_form_data['username'] = username
        login_form_data['password'] = password

        logged_in_response = session.request(
            login_form.method,
            login_form.action,
            data=login_form_data,
        )

        logged_in_page = html.document_fromstring(logged_in_response.content)
        if logged_in_page.cssselect('form.login-form'):
            raise InvalidCredentialsException()

        points_elem = logged_in_page.cssselect('.points')
        if not points_elem:
            # We don't know what went wrong here.
            raise RuntimeError()

        points_text = ''.join(points_elem[0].itertext())
        points_match = RE_POINTS.search(points_text)
        if not points_match:
            # We don't know what went wrong here either.
            raise RuntimeError()

        return int(points_match.group('points'))
