import pytest
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from .data.pdf_download_data import HTML_TEXT, YEAR_LINKS

from bike_rack.check_page_setup import check_page_setup


class TestCheckPageSetup:
    """Tests check_page_setup() which confirms that the current layout of
    the BOE page still matches the expected layout
    """

    @pytest.mark.parametrize(
        'url, expected',
        [('https://comptroller.baltimorecity.gov/boe/meetings/minutes',
          {'pass': ['request', 'html_parsing'],
           'fail': [],
           'error_message': None}),
         ('https://comptroller.baltimorecity.gov/boe/fake-path',
          {'pass': [],
           'fail': ['request'],
           'error_message': 'Not Found'})]
    )
    def test_check_page_setup(self, url, expected):
        """Tests check_page_setup() with several different urls
        """

        # runs function on input url and captures return values
        checks, soup = check_page_setup(url)

        # checks that the checks returned by the function match expected
        print('EXPECTED')
        pprint(expected)
        print('OUTPUT')
        pprint(checks)
        assert checks == expected

        # checks that the soupified page is returned
        if 'html_parsing' in checks['pass']:
            assert soup is not None

    def test_year_div(self):
        """Tests that the div containing the links to the minutes page for
        each year exists on the page

        TEST DATA
        - N/A

        TEST DATA
        - N/A

        ASSERTIONS
        - assert that a div with class 'field field-name-body'
        - assert that there is a <p> tag with links that follow a year format
        """
        assert 1

    def test_minute_div(self):
        """Tests that the div containing the links to each meeting's minutes
        exists on the page

        TEST DATA
        - N/A

        TEST DATA
        - N/A

        ASSERTIONS
        - assert that a div with class 'field field-name-body'
        - assert that there is a <p> tag with links that follow the
          meeting link format
        """
        assert 1

class TestGetYearLinks:
    """Tests get_year_links() that retrieves the links to the pages that
    contain the meeting links for each year of BOE meetings
    """

    def test_get_year_links(self):
        """Tests the function that retrieves the list of links for each page
        on the Comptroller website that corresponds to a year of BOE meetings

        TEST DATA
        - A sample of the html scraped from a particular page
        - A known list of year links from the BOE page

        TEST SETUP
        - N/A

        ASSERTIONS
        - assert that the scraped links matches the list of known links
        """
        assert 1

    def test_exclude_non_year_links(self):
        """Tests the exclusion of other anchor tags on the page that match a
        format similar to that of the links for each year of minutes

        TEST DATA
        - A sample of the html scraped from a particular page
        - A list of anchor tags for each year in the sample html

        TEST SETUP
        - Add an anchor tag that matches the format of the year link to some
          part of the sample HTML data outside the div where year links are
          currently found

        ASSERTIONS
        - assert that the scraped links exclude the anchor tag added during
          the test setup
        """
        assert 1

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

class TestGetParseMeetingDate:
    """Tests parse_meeting_dates() which parses the meeting date from
    the anchor tags returned by the get_meeting_links() function
    """

    def test_standard_date_format(self):
        """Tests the parsing of the standard date format in the anchor tags

        TEST DATA
        - A list of anchor tag that each contains the meeting date
          in a standard format

        TEST SETUP
        - N/A

        ASSERTIONS
        - assert that the long date is parsed into the correct format
        """
        assert 1

    def test_single_letter_deletions(self):
        """Tests the parsing of dates in which the anchor tag is missing
        a letter of the month, e.g. 'une' instead of 'June'

        TEST DATA
        - A list of anchor tag that each contains the meeting date
          in a standard format

        TEST SETUP
        - Modify the text of the anchor tags to remove a single letter

        ASSERTIONS
        - assert that modified anchor tags are parsed correctly
        """
        assert 1

class TestCheckFileList:
    """Tests check_file_list() which checks the list of downloaded pdfs
    and returns a list of pdfs that still need to be downloaded
    """

    def test_no_missing_pdfs(self):
        """Tests that the function returns nothing when all pdfs are present

        TEST DATA
        - A list of file names to populate the temporary directory with
        - A list of anchor tags to check the directory against

        TEST SETUP
        - Create a temporary directory to store the downloaded files
          More information: https://docs.pytest.org/en/stable/tmpdir.html
        - Populate the directory from the list of file names

        ASSERTIONS
        - assert that the the function returns nothing since all of the files
          are already present in the directory
        """
        assert 1

    def test_missing_pdf(self):
        """Tests that function returns the list of pdfs that are missing
        from the directory

        TEST DATA
        - A list of file names to populate the temporary directory with
        - A list of anchor tags to check the directory against

        TEST SETUP
        - Create a temporary directory to store the downloaded files
          More information: https://docs.pytest.org/en/stable/tmpdir.html
        - Populate the directory with all but one of the files from the list

        ASSERTIONS
        - assert that the the function returns the anchor tag associated with
          the file that is missing from the directory
        """
        assert 1

    def test_extra_pdf(self):
        """Tests that function returns the file name of the pdf that isn't
        in the list of anchor tags that are supposed to be in the directory

        TEST DATA
        - A list of file names to populate the temporary directory with
        - A list of anchor tags to check the directory against

        TEST SETUP
        - Create a temporary directory to store the downloaded files
          More information: https://docs.pytest.org/en/stable/tmpdir.html
        - Populate the directory from the list of file names
        - Add another file to the directory

        ASSERTIONS
        - assert that the the function returns the name of the file that isn't
          in the list of the anchor tags
        """
        assert 1

class TestDownloadPDF:
    """Tests the function that downloads and stores any missing pdfs returned
    by check_file_list() in the directory of downloaded pdfs
    """

    def test_download(self):
        """Tests the download of a pdf from a meeting link specified
        in the test data

        TEST DATA
        - An anchor tag which contains a link to a pdf of minutes

        TEST SETUP
        - Create a temporary directory to store the downloaded file
          More information: https://docs.pytest.org/en/stable/tmpdir.html

        ASSERTIONS
        - assert that the file is downloaded without errors
        - assert that the file has the correct filename
        """
        assert 1

    def test_error_in_link(self):
        """Tests error handling for a pdf link that has an issue with it

        TEST DATA
        - An anchor tag which contains a link to a pdf of minutes

        TEST SETUP
        - Create a temporary directory to store the downloaded file
          More information: https://docs.pytest.org/en/stable/tmpdir.html
        - Modify the link to cause a error that would prevent downloading

        ASSERTIONS
        - assert that the appropriate error message is raised when trying to
          download the file specified by the link
        """
        assert 1
