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


class TestDownloadPDF:
    """Tests download_pdf() which downloads and stores any missing pdfs returned
    by check_missing_pdfs() in the directory of downloaded pdfs
    """

    def test_valid_url(self, pdf_dir):
        """Tests the download of a pdf from a meeting link specified
        in the test data
        """
        # input
        year = "2021"
        date = "2021-01-20"
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        # setup
        del_dir_contents(pdf_dir)
        assert is_empty(pdf_dir)
        pdf_name = date.replace("-", "_") + ".pdf"
        pdf_file = pdf_dir / year / pdf_name

        # execution
        passed, message, file = download_pdf(year, date, url, dir=pdf_dir)
        print("ERROR")
        print(message)

        # validation
        assert passed
        assert file is not None
        assert pdf_file.exists()
        assert file == pdf_file

    def test_missing_pdf_dir(self, pdf_dir):
        # input
        year = "2021"
        date = "2021-01-20"
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        # setup
        del_dir_contents(pdf_dir)
        pdf_dir.rmdir()
        assert pdf_dir.exists() is False
        pdf_name = date.replace("-", "_") + ".pdf"
        pdf_file = pdf_dir / year / pdf_name

        # execution
        passed, message, file = download_pdf(year, date, url, dir=pdf_dir)
        print("ERROR")
        print(message)

        # validation
        assert passed
        assert file is not None
        assert pdf_file.exists()
        assert file == pdf_file

    def test_non_pdf_url(self, pdf_dir):
        """Tests that the function returns False when given a url that doesn't
        point to a pdf
        """
        # input
        year = "2021"
        date = "2021-01-20"
        url = "https://www.google.com/"

        # setup
        del_dir_contents(pdf_dir)
        assert is_empty(pdf_dir)
        pdf_name = date.replace("-", "_") + ".pdf"
        pdf_file = pdf_dir / year / pdf_name

        # execution
        passed, message, file = download_pdf(year, date, url, dir=pdf_dir)

        # validation
        assert not passed
        assert file is None
        assert pdf_file.exists() is False
        assert message == f"The content stored at {url} is not a pdf"

    @pytest.mark.parametrize(
        "url", [" ", "https://requests.readthedocs.io/quickstart/barney"]
    )
    def test_invalid_url(self, pdf_dir, url):
        """Tests that the function returns False when given a url that raises
        an error when being requested
        """
        # input
        year = "2021"
        date = "2021-01-20"

        # setup
        del_dir_contents(pdf_dir)
        assert is_empty(pdf_dir)
        pdf_name = date.replace("-", "_") + ".pdf"
        pdf_file = pdf_dir / year / pdf_name

        # execution
        passed, message, file = download_pdf(year, date, url, dir=pdf_dir)
        print("ERROR")
        print(message)

        # validation
        assert not passed
        assert file is None
        assert pdf_file.exists() is False
        assert message[:28] == "An error occurred requesting"
