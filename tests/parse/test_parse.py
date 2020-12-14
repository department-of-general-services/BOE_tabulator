import pytest
import PyPDF2
from pathlib import Path

from common.parse_utils import Minutes, parse_pdf
from tests.parse.parse_data import RAW_TEXT, CLEAN_TEXT, AGREEMENTS


class TestMinutes:
    """Tests the Minutes class and its methods"""

    @pytest.mark.parametrize(
        "pdf_path,page_count,meeting_date",
        [
            ("tests/parse/2010_03_17.pdf", 105, "2010-03-17"),
            ("tests/parse/2013_11_20.pdf", 209, "2013-11-20"),
        ],
    )
    def test_init(self, pdf_path, page_count, meeting_date):

        path = Path(pdf_path)
        minutes = Minutes(path)

        assert page_count == minutes.page_count
        assert meeting_date == minutes.meeting_date

    @pytest.mark.parametrize(
        "date,raw,clean",
        [
            ("2010-03-17", RAW_TEXT["2010"], CLEAN_TEXT["2010"]),
            ("2013-11-20", RAW_TEXT["2013"], CLEAN_TEXT["2013"]),
        ],
    )
    def test_parse_and_clean_pages(self, minutes, date, raw, clean):

        min = minutes[date]

        min.parse_and_clean_pages()

        print("RAW OUTPUT")
        print(min.raw_text[:100])
        print("RAW EXPECTED")
        print(raw)

        print("CLEAN OUTPUT")
        print(min.clean_text[:100])
        print("CLEAN EXPECTED")
        print(clean)

        assert min.raw_text is not None
        assert min.clean_text is not None
        assert min.raw_text[:100] == raw
        assert min.clean_text[:100] == clean

    @pytest.mark.parametrize(
        "date,expected,count",
        [
            # ("2010-03-17", AGREEMENTS["2010"], 3),
            # ("2013-11-20", AGREEMENTS["2013"], 3),
            ("2020-01-15", AGREEMENTS["2020"], 3),
        ],
    )
    def test_get_agreements(self, minutes, date, expected, count):
        min = minutes[date]

        min.get_agreements()

        assert len(min.agreements) == count

        for i, agreement in enumerate(min.agreements[:5]):
            print(f"EXPECTED {i}")
            print(expected[i])
            print(f"OUTPUT {i}")
            print(agreement[:5])
        assert 0


class TestParsePDF:
    """Tests the parse_pdf function which instantiates a Minutes object
    then calls parse_pages() and clean_pages() methods"""

    @pytest.mark.parametrize(
        "pdf_path", ["tests/parse/2010_03_17.pdf", "tests/parse/2013_11_20.pdf"]
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
            ("tests/parse/fake_name.pdf", ValueError),
            ("tests/parse/fake_name2.pdf", FileNotFoundError),
        ],
    )
    def test_parse_pdf_error(self, pdf_path, exception):
        path = Path(pdf_path)
        with pytest.raises(exception):
            parse_pdf(path)
