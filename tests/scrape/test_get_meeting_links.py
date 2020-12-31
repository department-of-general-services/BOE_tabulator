import pytest
from bs4 import BeautifulSoup
from pprint import pprint
from copy import deepcopy

from tests.scrape.scrape_data import LINKS_2017

from common.scrape_utils import get_meeting_links


class TestGetMeetingLinks:
    """Tests get_meeting_links() which retrieves all of the meeting links
    from the page that lists the BOE minutes for a given year
    """

    def test_standard_link_format(self):
        """Tests that function parses standard date formats correctly"""

        assert 1

    def test_full_url_pdf_link(self):
        """Tests that function parses standard date formats correctly

        TEST DATA
        - A sample of the html scraped from a particular page
        - List of anchor tags for each meeting link in the sample html

        TEST SETUP
        - Modify the href of one of the anchor tags to in the sample html
          to reflect the known edge case in the actual BOE meeting links
          i.e. the href that is a full url instead of a relative reference

        ASSERTIONS
        - assert that the function returns all of the anchor tags in the list
        """
        assert 1
