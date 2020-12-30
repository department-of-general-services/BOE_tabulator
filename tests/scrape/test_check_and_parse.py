import pytest
from pprint import pprint


from common.scrape_utils import check_and_parse_page


class TestCheckAndParsePage:
    """Tests check_and_parse_page() which confirms that the current layout of
    the BOE page still matches the expected layout and returns a BeautifulSoup
    object of the parsed html
    """

    @pytest.mark.parametrize(
        "url, expected",
        [
            (
                "https://comptroller.baltimorecity.gov/boe/meetings/minutes",
                {
                    "pass": ["request", "html_parsing"],
                    "fail": [],
                    "error_message": None,
                },
            ),
            (
                "https://comptroller.baltimorecity.gov/boe/fake-path",
                {"pass": [], "fail": ["request"], "error_message": "Not Found"},
            ),
        ],
    )
    def test_check_and_parse_page(self, url, expected):
        """Tests check_and_parse_page() with several different urls"""

        # runs function on input url and captures return values
        checks, soup = check_and_parse_page(url)

        # checks that the checks returned by the function match expected
        print("EXPECTED")
        pprint(expected)
        print("OUTPUT")
        pprint(checks)
        assert checks == expected

        # checks that the soupified page is returned
        if "html_parsing" in checks["pass"]:
            assert soup is not None
