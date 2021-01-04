from pprint import pprint
from common.scrape_utils import get_boe_pdfs


def test_get_boe_pdfs():
    # setup
    base_url = "https://comptroller.baltimorecity.gov"
    minutes_url = base_url + "/boe/meetings/minutes"

    # execution
    output = get_boe_pdfs(minutes_url, base_url)
    print(output)

    # validation

    assert 0
