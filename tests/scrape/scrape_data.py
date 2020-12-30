from pathlib import Path

# static sample of html text used for testing, scraped from
# https://comptroller.baltimorecity.gov/boe/meetings/minutes
html_path = Path.cwd() / "tests" / "scrape" / "sample_boe_page.html"
with open(html_path, "r") as file:
    HTML_TEXT = file.read()

# Example set of expected year links pulled from HTML_TEXT
YEAR_LINKS = {
    "2020": "/minutes-2020",
    "2019": "/2019",
    "2018": "/minutes-2018",
    "2017": "/boe/meetings/minutes",
    "2016": "/minutes-2016-0",
    "2015": "/minutes-2015",
    "2014": "/minutes-2014",
    "2013": "/minutes-2013",
    "2012": "/minutes-2012",
    "2011": "/minutes-2011",
    "2010": "/minutes-2010",
    "2009": "/minutes-2009",
}

# input to check_missing_pdfs()
MEETING_LINKS = {
    "2020": {
        "2020-01-15": "https://www.fake-path.com/2020-01-15",
        "2020-01-22": "https://www.fake-path.com/2020-01-22",
    },
    "2019": {
        "2019-01-09": "https://www.fake-path.com/2019-01-15",
        "2019-01-16": "https://www.fake-path.com/2019-01-08",
    },
}

# output of
