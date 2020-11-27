import pytest
import PyPDF2
from pathlib import Path

from bike_rack.parse_utils import Minutes


class TestMinutes:

    @pytest.mark.parametrize(
        'pdf_path,page_count,meeting_date',
        [('tests/data/2010_03_17.pdf', 105, '2010-03-17'),
         ('tests/data/2013_11_20.pdf', 209, '2013-11-20')]
    )
    def test_init(self, pdf_path, page_count, meeting_date):

        path = Path(pdf_path)
        minutes = Minutes(path)

        assert page_count == minutes.page_count
        assert meeting_date == minutes.meeting_date


    @pytest.mark.parametrize(
        'pdf_path',
        ['tests/data/2010_03_17.pdf',
         'tests/data/2013_11_20.pdf']
    )
    def test_parse_pages(self, pdf_path):

        path = Path(pdf_path)
        minutes = Minutes(path)

        minutes.parse_pages()
        assert minutes.parsed_text is not None
        print(minutes.parsed_text[:20])
        assert 0
