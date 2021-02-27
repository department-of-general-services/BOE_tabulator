import pytest
from pprint import pprint
from copy import deepcopy
from pathlib import Path

from tests.scrape.scrape_data import MEETING_LINKS

from common.utils import del_dir_contents, is_empty
from common.scrape_utils import check_missing_pdfs


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
                pdf_name = date + ".pdf"
                pdf_file = year_dir / pdf_name
                pdf_file.touch(exist_ok=True)
                assert pdf_file.exists()
                files.append(pdf_file)
        return files

    def test_no_missing_pdfs(self, pdf_dir):
        """Tests that the function returns nothing when all pdfs are present"""
        # setup
        pdf_files = self._create_pdf_files(pdf_dir, MEETING_LINKS)
        print(pdf_files)

        # execution
        missing, extra = check_missing_pdfs(MEETING_LINKS, dir=pdf_dir)

        # validation
        assert not missing
        assert not extra

    @pytest.mark.parametrize(
        "year,date,link",
        [
            ("2020", "2020_01_15", "https://www.fake-path.com/2020-01-15"),
            ("2019", "2019_01_09", "https://www.fake-path.com/2019-01-15"),
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
        missing_name = date + ".pdf"
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
        date = "2020_01_15"
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

    def test_non_dir_item(self, pdf_dir):
        """Tests that a non directory item at the top level pdf_dir won't throw
        an error when checking for extra pdfs
        """
        # setup
        pdf_files = self._create_pdf_files(pdf_dir, MEETING_LINKS)
        extra_file = pdf_dir / "extra.txt"
        print(pdf_files)
        extra_file.touch()
        assert extra_file.exists()

        # execution
        missing, extra = check_missing_pdfs(MEETING_LINKS, dir=pdf_dir)

        # validation
        assert not missing
        assert not extra
