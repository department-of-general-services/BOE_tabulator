import pytest
from bs4 import BeautifulSoup
from pprint import pprint
from copy import deepcopy
from pathlib import Path

from tests.scrape.scrape_data import HTML_TEXT, YEAR_LINKS, MEETING_LINKS

from common.utils import del_dir_contents
from common.scrape_utils import (
    get_year_links,
    check_and_parse_page,
    parse_long_dates,
    check_missing_pdfs,
    MONTHS,
)


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


class TestParseLongDates:
    """Tests parse_meeting_dates() which parses the meeting date from
    the anchor tags returned by the get_meeting_links() function
    """

    @pytest.mark.parametrize(
        "input_date,output_date",
        [
            ("November 10, 2020", "2020_11_10"),  # checks standard date
            ("April 6, 2020", "2020_04_06"),  # checks for zero padding
            ("une 17, 2019", "2019_06_17"),  # checks for single letter deletion
            ("Mrach 2, 2018", "2018_03_02"),  # checks for swapped letters
        ],
    )
    def test_parse_long_dates(self, input_date, output_date):
        """Tests parse_long_dates() against the standard date format
        plus all of the edge cases we've seen
        """
        parsed, date = parse_long_dates(input_date)

        print(f"date {date}")

        assert date == output_date
        assert parsed

    @pytest.mark.parametrize(
        "input_date,error_message",
        [(" ", "' ' is not a parseable date")],  # checks whitespace links
    )
    def test_fail_on_unparseable_date(self, input_date, error_message):
        """Tests that parse_long_dates() raises an error when it is passed
        an unparseable date
        """
        parsed, output = parse_long_dates(input_date)

        assert not parsed
        assert output == error_message


class TestCheckMissingPDFs:
    """Tests check_missing_pdfs() which checks the list of downloaded pdfs
    and returns a list of pdfs that still need to be downloaded
    """

    def _create_pdf_files(self, dir, meeting_dict):
        """Helper function used to populate pdf_dir"""
        files = []
        for year, meetings in meeting_dict.items():
            year_dir = dir / year
            year_dir.mkdir(exist_ok=True)
            for date in meetings:
                pdf_name = date.replace("-", "_") + ".pdf"
                pdf_file = year_dir / pdf_name
                pdf_file.touch(exist_ok=True)
                assert pdf_file.exists()
                files.append(pdf_file)
        return files

    def test_no_missing_pdfs(self, pdf_dir):
        """Tests that the function returns nothing when all pdfs are present"""
        # setup
        pdf_files = self._create_pdf_files(pdf_dir, MEETING_LINKS)
        for file in pdf_files:
            assert file.exists()

        # execution
        missing, extra = check_missing_pdfs(MEETING_LINKS, dir=pdf_dir)

        # validation
        assert not missing
        assert not extra

    @pytest.mark.parametrize(
        "year,date,link",
        [
            ("2020", "2020-01-15", "https://www.fake-path.com/2020-01-15"),
            ("2019", "2019-01-09", "https://www.fake-path.com/2019-01-15"),
        ],
    )
    def test_missing_pdf(self, pdf_dir, year, date, link):
        """Tests that function returns the list of pdfs that are missing
        from the directory"""
        # input
        missing_links = {year: {date: link}}

        # setup - create all but one pdf
        keep_links = deepcopy(MEETING_LINKS)
        del keep_links[year][date]  # removes one pdf from dict
        del_dir_contents(pdf_dir)
        pdf_files = self._create_pdf_files(pdf_dir, keep_links)
        for file in pdf_files:
            assert file.exists()
        missing_name = date.replace("-", "_") + ".pdf"
        missing_file = pdf_dir / missing_name
        assert missing_file.exists() is False

        # execution
        print("INPUT")
        pprint(MEETING_LINKS)
        missing, extra = check_missing_pdfs(MEETING_LINKS, dir=pdf_dir)
        print("OUTPUT")
        pprint(missing)
        print("EXPECTED")
        pprint(missing_links)

        # validation
        assert missing == missing_links
        assert not extra

    def test_extra_pdf(self, pdf_dir):
        """Tests that function returns the file name of the pdf that isn't
        in the list of meetings that are supposed to be in the directory
        """
        # input
        year = "2020"
        date = "2020-01-15"
        expected = {"2020_01_15.pdf"}

        # setup
        pdf_files = self._create_pdf_files(pdf_dir, MEETING_LINKS)
        for file in pdf_files:
            assert file.exists()
        input_links = deepcopy(MEETING_LINKS)
        del input_links[year][date]

        # execution
        print("INPUT")
        pprint(input_links)
        missing, extra = check_missing_pdfs(input_links, pdf_dir)

        # validation
        assert not missing
        assert extra == expected


class TestDownloadPDF:
    """Tests download_pdf() which downloads and stores any missing pdfs returned
    by check_missing_pdfs() in the directory of downloaded pdfs
    """

    def test_valid_url(self):
        """Tests the download of a pdf from a meeting link specified
        in the test data
        """
        assert 1

    def test_non_pdf_url(self):
        """Tests that the function returns False when given a url that doesn't
        point to a pdf
        """
        assert 1

    def test_invalid_url(self):
        """Tests that the function returns False when given a url that raises
        an error when being requested
        """
        assert 1
