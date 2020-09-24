

class TestPageSetup:
    """Tests that the setup of the BOE page still matches the layout that
    these scraping functions were written for
    """

    def test_year_div(self):
        assert 1

    def test_minute_div(self):
        assert 1

class TestGetYearLinks:

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

    def test_non_year_digit_link(self):
        """Tests the exclusion of other anchor tags on the page that match a
        format similar to that of the links for each year of minutes

        TEST DATA
        - A sample of the html scraped from a particular page
        - A known list of year links from the BOE page

        TEST SETUP
        - Add an anchor tag that matches the format of the year link to some
          part of the sample HTML data outside the div where year links are
          currently found
        """

class TestGetMeetingLinks:
    def test_standard_link_format(self):
        """Tests the function
        """
        assert 1

    def test_full_url_pdf_link(self):
        assert 1

class TestGetParseMeetingDate:
    def test_parse_meeting_date(self):
        assert 1

    def test_single_letter_deletions(self):
        assert 1

class TestDownloadPDFs:

    def test_check_pdf_list(self):
        assert 1

    def test_download_pdf(self):
        assert 1
