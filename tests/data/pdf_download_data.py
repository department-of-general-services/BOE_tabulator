from .sample_boe_page import HTML_TEXT

# static sample of html text used for testing, scraped from
# https://comptroller.baltimorecity.gov/boe/meetings/minutes
SAMPLE_HTML = HTML_TEXT

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
