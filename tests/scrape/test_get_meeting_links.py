import pytest
import re
from bs4 import BeautifulSoup
from pprint import pprint
from copy import deepcopy

from tests.scrape.scrape_data import HTML_TEXT, LINKS_2017

from common.scrape_utils import get_meeting_links, get_boe_pdfs


class TestGetMeetingLinks:
    """Tests get_meeting_links() which retrieves all of the meeting links
    from the page that lists the BOE minutes for a given year
    """

    def test_get_meeting_links(self):
        """Tests that function parses standard date formats correctly"""
        # setup
        expected = LINKS_2017
        soup = BeautifulSoup(HTML_TEXT, "html.parser")
        duplicate_dates = soup.find_all("a", text="June 12, 2017")
        absolute_links = soup.find_all("a", href=re.compile("https://"))
        assert len(duplicate_dates) > 1
        assert absolute_links
        print(duplicate_dates)
        print(absolute_links)

        # execution
        output = get_meeting_links(soup, url="https://www.google.com")
        pprint(output)

        # validation
        assert output == expected
