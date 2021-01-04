from pprint import pprint
from pathlib import Path
from common.scrape_utils import get_boe_pdfs


def test_get_boe_pdfs():
    # input
    base_url = "https://comptroller.baltimorecity.gov"
    minutes_url = base_url + "/boe/meetings/minutes"
    file_name = "2020_01_08.pdf"

    # setup
    pdf_dir = Path.cwd() / "pdf_files"
    pdf_dir.mkdir(exist_ok=True)
    file = pdf_dir / "2020" / file_name
    if file.exists():
        file.unlink()
    assert file.exists() is False

    # execution
    output = get_boe_pdfs(minutes_url, base_url)
    downloads_2020 = output.get("2020", None)
    print("2020 files downloaded:")
    print(downloads_2020)

    # validation
    assert file.exists()
    assert file_name in downloads_2020
