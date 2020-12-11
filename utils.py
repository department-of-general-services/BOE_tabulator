import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import re
import PyPDF2
from datetime import datetime
import numpy as np

# adding throwaway comment to test pre-commit hook


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


# months is here because it is used in multiple places
months = (
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
    month_str, score = month_match_lev(month_str)
    month = str(months.index(month_str) + 1).zfill(2)

    # grab the back of the string to get the year
    year = date_re.group(3)  # grabs year from third capture group in regex
    day = date_re.group(2)  # grabs day from second capture group in regex

    # converts year and day to string
    year = str(year)
    day = str(day).zfill(2)

    return True, "_".join([year, month, day])


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


def store_pdf_text_to_df(path):
    """Finds .pdf files stored at the given url and stores them within the
    repository for later analysis.

    Args:
        base_url (str): The main url for the Comptroller of Baltimore's webiste
        minutes_url (str): The url where the function can find links to pages of
        pdf files organized by year
    Returns:
        None: This is a void function.
    """
    pdf_paths = list(path.rglob("*.pdf"))
    text_df = pd.DataFrame(columns=["date", "page_number", "minutes"])
    for pdf_path in pdf_paths:
        # print(f"Parsing file: {pdf_path.name}")
        minutes = ""
        pdfFileObj = open(pdf_path, "rb")
        try:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
        except ValueError:
            print(f"An error occurred reading file {pdf_path}")
        for page in pdfReader.pages:
            minutes += page.extractText().strip()

        date_string = pdf_path.stem
        date = datetime.strptime(date_string, "%Y_%m_%d").date()
        page_number = re.findall(r"(^[0-9]+)", minutes)
        if page_number:
            page_number = page_number[0]
        else:
            page_number = ""
        try:
            row = {"date": date, "page_number": page_number, "minutes": minutes.strip()}
            text_df = text_df.append(row, ignore_index=True)
        except ValueError:
            print(f"No date found for file {pdf_path}")
    print(f"Wrote {len(text_df)} rows to the table of minutes.")
    return text_df


def is_empty(_dir: Path) -> bool:
    return not bool([_ for _ in _dir.iterdir()])


def replace_chars(text):
    replacements = [
        ("Œ", "-"),
        ("ﬁ", '"'),
        ("ﬂ", '"'),
        ("™", "'"),
        ("Ł", "•"),
        (",", "'"),
        ("Š", "-"),
        ("€", " "),
        ("¬", "-"),
        ("–", "…"),
        ("‚", "'"),
        ("Ž", "™"),
        ("˚", "fl"),
        ("˜", "fi"),
        ("˛", "ff"),
        ("˝", "ffi"),
        ("š", "—"),
        ("ü", "ti"),
        ("î", "í"),
        ("è", "c"),
        ("ë", "e"),
        ("Ð", "–"),
        ("Ò", '"'),
        ("Ó", '"'),
        ("Õ", "'"),
    ]
    for i in replacements:
        text = text.replace(i[0], i[1])
    return text


def del_dir_contents(root):
    """Convenience function so we don't have to empy out pdf_dir by hand
    during testing.

    Removes all
    """
    for p in root.iterdir():
        if p.is_dir():
            del_dir_contents(p)
        else:
            p.unlink()
    for p in root.iterdir():
        if p.is_dir():
            p.rmdir()
    return


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


def lev(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def month_match_lev(text):
    """
    Args:
        text (str): the misspelled month string

    Returns:
        best_match (str): the month string that best matches the misspelled input
        best_score (int): the Levenshtein distance between text and best_match
    """
    text = text.lower()
    best_match = ""
    best_score = 9999  # lower scores are better
    for i in months:
        # lev dist == num changes to make text into i
        score = lev(text, i)
        if score < best_score:
            best_score = score
            best_match = i

    return best_match, best_score
