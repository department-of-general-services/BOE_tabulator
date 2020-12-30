import pytest

from common.scrape_utils import parse_meeting_date


class TestParseMeetingDate:
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
            ("March 2, 2019D", "2019_03_02"),  # checks for excluding end char
        ],
    )
    def test_parse_meeting_date(self, input_date, output_date):
        """Tests parse_meeting_date() against the standard date format
        plus all of the edge cases we've seen
        """
        parsed, date = parse_meeting_date(input_date)

        print(f"date {date}")

        assert date == output_date
        assert parsed

    @pytest.mark.parametrize(
        "input_date,error_message",
        [(" ", "' ' is not a parseable date")],  # checks whitespace links
    )
    def test_fail_on_unparseable_date(self, input_date, error_message):
        """Tests that parse_meeting_date() raises an error when it is passed
        an unparseable date
        """
        parsed, output = parse_meeting_date(input_date)

        assert not parsed
        assert output == error_message
