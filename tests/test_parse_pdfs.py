import pytest
import PyPDF2

# from bike_rack.minutes import Minutes


class TestBOEMinutes:

    def test_initialize_boe_minutes(self):

        pdf_path = 'tests/data/2010_3_17.pdf'
        page_count = 105
        meeting_date = '2020-03-17'

        Minutes = PyPDF2.PdfFileReader(pdf_path)
        assert page_count == Minutes.numPages

        Page1 = Minutes.getPage(1)
        print(Page1.extractText())
        assert 0
