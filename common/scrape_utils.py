import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
from datetime import datetime
from collections import defaultdict

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

BASE_URL = "https://comptroller.baltimorecity.gov"


def get_boe_pdfs(minutes_url, base_url=BASE_URL):
    """Finds .pdf files stored at the given url and stores them within the
    repository for later analysis.
    Args:
        base_url (str): The main url for the Comptroller of Baltimore's webiste
        minutes_url (str): The url where the function can find links to
            pages of pdf files organized by year
    Returns:
        missing_pdsf: The dictionary of pdfs that were downloaded
    """

    # get the links to each year of BOE meetings
    passed, error, boe_page = check_and_parse_page(minutes_url)
    if not passed:
        print(error)
        return
    year_links = get_year_links(boe_page)
    if not year_links:
        print(f"No year links found at {minutes_url}")

    # get the links to the minutes for each meeting
    meeting_links = {}
    for year, link in year_links.items():
        passed, error, page = check_and_parse_page(link)
        if not passed:
            print(error)
            continue
        meetings = get_meeting_links(page, link)
        meeting_links[year] = meetings

    # check which meetings still need to be downloaded
    missing_pdfs, extra_pdfs = check_missing_pdfs(meeting_links)
    if extra_pdfs:
        print(f"These extra pdfs were found in the directory {extra_pdfs}")
    if not missing_pdfs:
        print("No new BOE minutes to download")
        return None

    # download missing pdfs
    counter = 0
    downloaded_pdfs = defaultdict(list)
    for year, meetings in missing_pdfs.items():
        for date, link in meetings.items():
            passed, error, file = download_pdf(year, date, link)
            if not passed:
                print(error)
                continue
            else:
                downloaded_pdfs[year].append(file.name)
                counter += 1
    print(f"Wrote {counter} pdf files to local repo.")
    return downloaded_pdfs


def check_and_parse_page(url):
    """Tries to requests and parses a url into a BeautifulSoup object

    Args:
        url: Link to the page to request and parse
    Returns:
        passed: Boolean indicating whether or not the checks passed
        message: Message indicating either the success or error
        soup: BeautifulSoup object of the parsed page
    """
    # checks if request went through successfully
    response = requests.get(url)
    if not response.status_code == 200:
        error = f"Encountered an issue accessing '{url}': {response.reason}"
        return False, error, None

    # parses HTML from response text
    soup = BeautifulSoup(response.text, "html.parser")

    message = f"'{url}' was successfully requested and parsed"
    return True, message, soup


def get_year_links(start_soup):
    """Grabs the link to each page of BOE meetings

    Args:
        start_soup (BeautifulSoup object): the beautifulsoup object that
        parses the "landing page" for the minutes links

    Returns:
        year_links (dict): dictionary with the years (2009, 2010, ...,
        current year) as keys and absolute links as values
    """
    # this eliminates the need to specify the years to grab since
    # four-digit years are used consistently
    year_tags = start_soup.find_all(
        "a", href=True, text=re.compile(r"^20\d{2}$")
    )  # find the tags that link to the minutes for specific years
    year_links = {}
    for tag in year_tags:
        year = tag.string
        link = tag.get("href")
        if not link.startswith(BASE_URL):
            link = BASE_URL + link  # converts relative links to absolute
        year_links[year] = link
    return year_links


def parse_meeting_date(date_string):
    """Extracts three simple strings representing the year, month, and day
    from a date in the  in the long format like 'November 19, 2010'.

    Args:
        date_string (str): The date in 'long' format
    Returns:
        passed: Boolean indicated whether or not the date was parsed
        date: Date parsed into format 'YYYY_MM_DD'
        message: Indicating the success or failure of parsing the date
    """

    # organizes date string into capture groups
    month, date, year = r"(\w*)", r"(\d{1,2})", r"(\d{4})"
    space, non_decimal = r"\s+", r"\D*"
    date_regex = month + space + date + non_decimal + year
    date_re = re.search(date_regex, date_string, re.IGNORECASE)

    # check that date is parseable
    if date_re is None:
        error = f"'{date_string}' is not a parseable date"
        return False, None, error

    # grabs the month.lower() from the regex match of the date_string
    month_str = date_re.group(1).lower()
    month_str, score = levenshtein_match(month_str, MONTHS)
    month = str(MONTHS.index(month_str) + 1).zfill(2)

    # grabs year and day from the regex
    year = date_re.group(3)
    day = date_re.group(2)

    # converts year and day to string
    year = str(year)
    day = str(day).zfill(2)

    # puts date into YYYY_MM_DD format
    date = "_".join([year, month, day])
    message = f"Successfully parsed {date_string} into {date}"

    return True, date, message


def check_missing_pdfs(meeting_links, dir=None):
    """Checks the downloaded pdfs against a list of parsed meeting links and
    returns any pdfs which are missing

    Args:
        meeting_links: Nested dict of year and the links to pdfs of the BOE
        meetings in that year
        dir: Path to directory that contains the pdf_files, defaults to current
        working directory

    Returns:
        missing_links: Nested dict of pdfs that still need to be downloaded
        extra_pdfs: List of downloaded pdfs not listed in the meeting links
    """
    missing_links = defaultdict(dict)
    expected_pdfs = set()
    downloaded_pdfs = set()

    # sets the directory and checks if it it exists
    if not dir:
        dir = Path.cwd() / "pdf_files"
    if not dir.exists():
        return meeting_links, None

    # checks for any missing pdfs
    for year, meetings in meeting_links.items():
        year_dir = dir / year
        for date, link in meetings.items():
            pdf_name = date + ".pdf"
            expected_pdfs.add(pdf_name)
            pdf_file = year_dir / pdf_name
            if not pdf_file.exists():
                missing_links[year][date] = link

    # checks for any extra pdfs
    for sub in dir.iterdir():
        if sub.is_dir():
            for pdf in sub.iterdir():
                downloaded_pdfs.add(pdf.name)
    extra_pdfs = downloaded_pdfs - expected_pdfs

    return missing_links, extra_pdfs


def download_pdf(year, date, url, dir=None):
    """Downloads a pdf from the given url and stores it in the sub-directory
    for the year in which the meeting occurred

    Args:
        year: Year in which the BOE meeting occurred
        date: Date on which BOE meeting occurred, with format YYYY-MM-DD
        url: Link to download the pdf of the minutes

    Returns:
        passed: Boolean value indicating if the download was successful
        message: Message describing the error or success of the download
        pdf_file: Path to downloaded file
    """
    # checks that url is valid
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error = f"An error occurred requesting {url}: {e}"
        return False, error, None

    # checks that the response is a pdf
    content_type = response.headers["content-type"]
    if "pdf" not in content_type:
        error = f"The content stored at {url} is not a pdf"
        return False, error, None

    # creates path to file
    if not dir:
        dir = Path.cwd() / "pdf_files"
    year_dir = dir / year
    pdf_name = date + ".pdf"
    pdf_file = year_dir / pdf_name

    # creates the year directory and writes the file to it
    try:
        year_dir.mkdir(parents=True, exist_ok=True)
        with open(pdf_file, "wb") as f:
            f.write(response.content)
    except TypeError as e:
        error = f"An error occurred with url {url}: {e}"
        return False, error, None

    message = f"Successfully saved pdf from {url}"
    return True, message, pdf_file


def get_meeting_links(soup, url):
    """Grabs the links to the minutes for each BOE meeting on a given page

    Args:
        soup (BeautifulSoup object): the beautifulsoup object that
        parses the "landing page" for each year of BOE meetings

    Returns:
        meeting_links (dict): dictionary with the dates of each BOE meeting
        as keys and absolute links to their minutes as values
    """

    meeting_links = {}
    meeting_tags = soup.find_all(name="a", href=re.compile("files"))

    for tag in meeting_tags:
        # parse the date
        date_str = tag.text.strip().encode("ascii", "ignore").decode("utf-8")
        passed, date, e = parse_meeting_date(date_str)
        if not passed:
            error = f"There was an issue parsing tag {tag} on page {url}: {e}"
            print(error)
            continue

        # extract link
        link = tag.get("href")
        if not link.startswith(BASE_URL):
            link = BASE_URL + link  # converts relative links to absolute

        # checks for duplicate dates
        # if they exist appends "meeting2" etc to date
        duplicates = [d for d in meeting_links.keys() if d.startswith(date)]
        if duplicates:
            date = date + f"_meeting{len(duplicates)+1}"
        meeting_links[date] = link

    return meeting_links
