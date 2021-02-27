import pytest
import os
from pathlib import Path

collect_ignore = ["scrape/test_get_boe_pdfs.py"]


@pytest.fixture(scope="session")
def pdf_dir(tmp_path_factory):
    basetemp = Path.cwd() / "temp_dir"
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(basetemp)
    basetemp.mkdir(parents=True, exist_ok=True)
    dir = tmp_path_factory.mktemp("pdf_files", numbered=False)
    print(dir)
    return dir
