import pytest
import PyPDF2
from pathlib import Path

from bike_rack.parse_utils import Minutes, parse_pdf, replace_chars, REPLACEMENTS
from tests.data.parse_pdfs_data import RAW_TEXT, CLEAN_TEXT


@pytest.mark.parametrize(
    "text,expected", [("March 17, 2010", "March 17, 2010"), ("ﬁquotesﬂ", '"quotes"')]
)
def test_replace_chars(text, expected):
    output = replace_chars(text, REPLACEMENTS)
    print("OUTPUT")
    print(output)
    print("EXPECTED")
    print(expected)
    assert output == expected


class TestMinutes:
    """Tests the Minutes class and its methods"""

    @pytest.mark.parametrize(
        "pdf_path,page_count,meeting_date",
        [
            ("tests/data/2010_03_17.pdf", 105, "2010-03-17"),
            ("tests/data/2013_11_20.pdf", 209, "2013-11-20"),
        ],
    )
    def test_init(self, pdf_path, page_count, meeting_date):

        path = Path(pdf_path)
        minutes = Minutes(path)

        assert page_count == minutes.page_count
        assert meeting_date == minutes.meeting_date

    @pytest.mark.parametrize(
        "pdf_path,expected",
        [
            ("tests/data/2010_03_17.pdf", RAW_TEXT["2010"]),
            ("tests/data/2013_11_20.pdf", RAW_TEXT["2013"]),
        ],
    )
    def test_parse_pages(self, pdf_path, expected):

        path = Path(pdf_path)
        minutes = Minutes(path)

        output = minutes.parse_pages()

        print("OUTPUT")
        print(output[:100])
        print("EXPECTED")
        print(expected)

        assert minutes.raw_text == output
        assert minutes.raw_text is not None
        assert output[:100] == expected

    @pytest.mark.parametrize(
        "pdf_path,expected",
        [
            ("tests/data/2010_03_17.pdf", CLEAN_TEXT["2010"]),
            ("tests/data/2013_11_20.pdf", CLEAN_TEXT["2013"]),
        ],
    )
    def test_clean_text(self, pdf_path, expected):
        path = Path(pdf_path)
        minutes = Minutes(path)

        raw_output = minutes.parse_pages()
        clean_output = minutes.clean_pages()

        print("RAW OUTPUT")
        print(raw_output[:100])
        print("CLEAN OUTPUT")
        print(clean_output[:100])
        print("EXPECTED")
        print(expected)

        assert raw_output != clean_output  # raw and clean text are different
        assert raw_output == minutes.raw_text  # raw text wasn't modified
        assert clean_output == minutes.clean_text  # output matches attribute
        assert clean_output[:100] == expected  # output matches expected


class TestParsePDF:
    """Tests the parse_pdf function which instantiates a Minutes object
    then calls parse_pages() and clean_pages() methods"""

    @pytest.mark.parametrize(
        "pdf_path", ["tests/data/2010_03_17.pdf", "tests/data/2013_11_20.pdf"]
    )
    def test_parse_pdf(self, pdf_path):
        path = Path(pdf_path)
        minutes = parse_pdf(path)

        print(minutes.raw_text[:10])
        print(minutes.clean_text[:10])

        # checks that both parse_pages() and clean_pages() are run
        assert minutes.clean_text is not None
        assert minutes.raw_text is not None

    @pytest.mark.parametrize(
        "pdf_path,exception",
        [
            ("tests/data/fake_name.pdf", ValueError),
            ("tests/data/fake_name2.pdf", FileNotFoundError),
        ],
    )
    def test_parse_pdf_error(self, pdf_path, exception):
        path = Path(pdf_path)
        with pytest.raises(exception):
            parse_pdf(path)
