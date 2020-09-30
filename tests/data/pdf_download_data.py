from .sample_boe_page import HTML_TEXT

# static sample of html text used for testing, scraped from
# https://comptroller.baltimorecity.gov/boe/meetings/minutes
SAMPLE_HTML = HTML_TEXT

# Example set of expected year links pulled from HTML_TEXT
YEAR_LINKS = ['<a href="/minutes-2020">2020</a>',
              '<a href="/2019">2019</a>',
              '<a href="/minutes-2018">2018</a>',
              '<a href="/boe/meetings/minutes">2017</a>',
              '<a href="/minutes-2016-0">2016</a>',
              '<a href="/minutes-2015">2015</a>',
              '<a href="/minutes-2014">2014</a>',
              '<a href="/minutes-2013">2013</a>',
              '<a href="/minutes-2012">2012</a>',
              '<a href="/minutes-2011">2011</a>',
              '<a href="/minutes-2010">2010</a>',
              '<a href="/minutes-2009">2009</a>']
