class BaseScraper(object):
    def scrape_balance(username, password):
        raise NotImplementedError()

class InvalidCredentialsException(Exception):
    pass
