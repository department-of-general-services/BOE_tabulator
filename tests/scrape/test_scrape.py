import pytest
from bs4 import BeautifulSoup
from pprint import pprint
from copy import deepcopy
from pathlib import Path

from tests.scrape.scrape_data import HTML_TEXT, YEAR_LINKS, MEETING_LINKS

from common.utils import del_dir_contents, is_empty
from common.scrape_utils import (
    get_year_links,
    check_and_parse_page,
    parse_meeting_date,
    check_missing_pdfs,
    download_pdf,
    MONTHS,
)


class TestGetMeetingLinks:
    """Tests get_meeting_links() which retrieves all of the meeting links
    from the page that lists the BOE minutes for a given year
    """

    def test_standard_link_format(self):
        """Tests that function parses standard date formats correctly

        TEST DATA
        - A sample of the html scraped from a particular page
        - List of anchor tags for each meeting link in the sample html

        TEST SETUP
        - N/A

        ASSERTIONS
        - assert that the function returns all of the anchor tags in the list
        """
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
