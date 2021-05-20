from bs4 import BeautifulSoup
from pprint import pprint

from tests.scrape.scrape_data import HTML_TEXT, YEAR_LINKS

from common.scrape_utils import get_year_links


class TestGetYearLinks:
    """Tests get_year_links() that retrieves the links to the pages that
    contain the meeting links for each year of BOE meetings
    """

    def test_get_year_links(self):
        """Tests the function that retrieves the list of links for each page
        on the Comptroller website that corresponds to a year of BOE meetings
        """
        # parses sample html for input to get_year_links() function
        soup = BeautifulSoup(HTML_TEXT, "html.parser")
        expected = YEAR_LINKS

        # runs get_year_links() function and captures output
        output = get_year_links(soup)

        # checks that the output of get_year_links matches the
        # expected list of annual links from the sample html
        print("EXPECTED")
        pprint(expected)
        print("OUTPUT")
        pprint(output)
        assert output == expected
