import pytest
from pathlib import Path
from common.parse_utils import Minutes

PDF_PATHS = [
    "tests/parse/2010_03_17.pdf",
    "tests/parse/2013_11_20.pdf",
    "tests/parse/2020_01_15.pdf",
]


@pytest.fixture(scope="session")
def minutes():
    minutes_dict = {}
    for path in PDF_PATHS:
        min = Minutes(Path(path))
        minutes_dict[min.meeting_date] = min
    print(minutes_dict)
    return minutes_dict
