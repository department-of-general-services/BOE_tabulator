import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
from datetime import datetime

from common.utils import levenshtein_match

# months is here because it is used in multiple places
MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)


def store_boe_pdfs(base_url, minutes_url):
    """Finds .pdf files stored at the given url and stores them within the
    repository for later analysis.
    Args:
        base_url (str): The main url for the Comptroller of Baltimore's webiste
        minutes_url (str): The url where the function can find links to
            pages of pdf files organized by year
    Returns:
        None: This is a void function.
    """

    checks, soup = check_and_parse_page(minutes_url)
    if checks["fail"]:
        print(f"Encountered an issue accessing {minutes_url}")
        print(f"Exiting due to the following error: {checks['error_message']}")
        return
    root = Path.cwd()
    pdf_dir = root / "pdf_files"
    total_counter = 0

    if not pdf_dir.is_dir():
        pdf_dir.mkdir(parents=True, exist_ok=False)

    year_links = get_year_links(soup)

    for year in year_links.keys():
        # make a directory for the files
        save_path = pdf_dir / str(year)
        save_path.mkdir(parents=True, exist_ok=True)
        # find all links where the associated text contains the year
        link = soup.find("a", href=True, text=str(year))
        annual_url = base_url + link["href"]
        print(f"Saving files from url: {annual_url}")
        # now follow the link to the page with that year's pdfs
        checks, soup_annual = check_and_parse_page(annual_url)
        if checks["fail"]:
            print(f"Encountered an issue accessing {annual_url}")
            print(
                "Escaping the current loop due to the following error: "
                f"{checks['error_message']}"
            )
            continue
        pdf_links = soup_annual.find_all(name="a", href=re.compile("files"))
        for idx, link in enumerate(pdf_links):
            pdf_location = link["href"]
            pdf_url = base_url + pdf_location
            pdf_file = requests.get(pdf_url)
            # derive name of the pdf file we're going to create
            # encoding and decoding removes hidden characters
            pdf_html_text = (
                link.get_text().strip().encode("ascii", "ignore").decode("utf-8")
            )
            # handle cases where the date is written out in long form
            parsed, pdf_date = parse_long_dates(pdf_html_text)
            if not parsed:
                print(pdf_date)  # error message
                continue
            pdf_filename = pdf_date + ".pdf"
            try:
                with open(save_path / pdf_filename, "wb") as f:
                    f.write(pdf_file.content)
                total_counter += 1
            except TypeError as err:
                print(f"an error occurred with path {pdf_location}: {err}")
    print(f"Wrote {total_counter} .pdf files to local repo.")
    return


def check_and_parse_page(url):
    response = requests.get(url)
    checks = {"pass": [], "fail": []}

    # checks if request went through successfully
    if response.status_code == 200:
        checks["pass"].append("request")
    else:
        checks["fail"].append("request")
        checks["error_message"] = response.reason
        return checks, None

    # tries to parse HTML from response text
    # Note: I've removed the try-except logic since no one has seen the error
    # we're trying to catch. If we get a parse error in the future, then
    # let's note the exception, restore the try-except, and catch it
    soup = BeautifulSoup(response.text, "html.parser")
    checks["pass"].append("html_parsing")

    # if all checks pass set error message to none and return checks
    checks["error_message"] = None
    return checks, soup


def get_year_links(start_soup):
    """
    Args:
        start_soup (BeautifulSoup object): the beautifulsoup object that
        parses the "landing page" for the minutes links

    Returns:
        year_links (dict): dictionary with the years (2009, 2010, ...,
        current year) as keys and relative links as values
    """
    # this eliminates the need to specify the years to grab since
    # four-digit years are used consistently
    year_tags = start_soup.find_all(
        "a", href=True, text=re.compile(r"^20\d{2}$")
    )  # find the tags that link to the minutes for specific years
    year_links = {
        tag.string: tag.get("href") for tag in year_tags
    }  # extracting the links

    return year_links


def parse_long_dates(date_string):
    """Extracts three simple strings representing the year, month, and day
    from a date in the  in the long format like 'November 19, 2010'.

    Args:
        date_string (str): The date in 'long' format
    Returns:
        year (str): The year as a four-character string
        month (str): The month as a string representing an int between 1 and 12
        day (str): The day as a string representing an int between 1 and 31
    """

    date_regex = re.compile(r"([\w]*)\s+(\d{1,2})\D*(\d{4})", re.IGNORECASE)
    date_re = date_regex.search(date_string)
    if date_re is None:
        return False, f"'{date_string}' is not a parseable date"
    """
    This regex captures any long date formats

    The components of the regex:
        (\w*) - First capture group, one or more word chars to find month
        \s - Space between month and date, not captured
        (\d{1,2}) - Second capture group, one or two numbers to find date
        \D* - Non decimal chars between date and year, not captured
        (\d{4}) - Third capture group, string of four numbers to find year
    """

    # check for garbage at the end of the string
    while not date_string[-1].isnumeric():
        date_string = date_string[:-1]

    # grabs the month.lower() from the regex match of the date_string
    month_str = date_re.group(1).lower()
    month_str, score = levenshtein_match(month_str, MONTHS)
    month = str(MONTHS.index(month_str) + 1).zfill(2)

    # grab the back of the string to get the year
    year = date_re.group(3)  # grabs year from third capture group in regex
    day = date_re.group(2)  # grabs day from second capture group in regex

    # converts year and day to string
    year = str(year)
    day = str(day).zfill(2)

    return True, "_".join([year, month, day])
