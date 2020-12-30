import pytest

from common.utils import del_dir_contents, is_empty
from common.scrape_utils import download_pdf


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
