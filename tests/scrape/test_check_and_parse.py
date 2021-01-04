import pytest
from pprint import pprint


from common.scrape_utils import check_and_parse_page


class TestCheckAndParsePage:
    """Tests check_and_parse_page() which confirms that the current layout of
    the BOE page still matches the expected layout and returns a BeautifulSoup
    object of the parsed html
    """

    def test_success(self):
        """Tests against a successful link"""
        # setup
        url = "https://comptroller.baltimorecity.gov/boe/meetings/minutes"
        expected = f"'{url}' was successfully requested and parsed"

        # execution
        passed, message, soup = check_and_parse_page(url)

        # validation
        assert passed
        assert message == expected
        assert soup is not None

    def test_request_fail(self):
        """Tests against a nonexistant link"""
        # setup
        url = "https://comptroller.baltimorecity.gov/boe/fake-path"
        expected = f"Encountered an issue accessing '{url}': Not Found"

        # execution
        passed, message, soup = check_and_parse_page(url)

        # validation
        assert not passed
        assert message == expected
        assert soup is None
