import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from pathlib import Path
import re
import PyPDF2
from datetime import datetime
import os
from enchant.utils import levenshtein

# months is here because it is used in multiple places
months = (
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december')

def parse_long_dates(date_string):
    """Extracts three simple strings representing the year, month, and day
    from a date in the  in the long format like 'November 19, 2010'.

    Args:
        date_string (str): The date in 'long' format
    Returns:
        year (str): The year as a four-character string
        month (str): The month as a string representing an integer between 1 and 12
        day (str): The day as a string representing an integer between 1 and 31
    """
    date_regex = re.compile(r'(\w*)\s+(\d{1,2})\D*(\d{4})', re.IGNORECASE)
    """
    This regex captures any long date formats

    The components of the regex:
        (\w*) - First capture group, one or more word chars to find month
        \s - Space between month and date, not captured
        (\d{1,2}) - Second capture group, one or two numbers to find date
        \D* - Non decimal chars between date and year, not captured
        (\d{4}) - Third capture group, string of four numbers to find year
    """
    date_re = date_regex.search(date_string)
    # check for garbage at the end of the string
    while not date_string[-1].isnumeric():
        date_string = date_string[:-1]
    
    # grabs the month.lower() from the regex match of the date_string
    month_str = date_re.group(1).lower()
    if month_str in months:  # if month was spelled correctly
        month = str(months.index(month_str)+1).zfill(2)
    else:  # if month wasn't spelled correctly
        # score is currently unused but present for compatibility
        month_str, score = month_match_lev(month_str)
        month = str(months.index(month_str)+1).zfill(2)
    
    # grab the back of the string to get the year
    year = date_string[-4:]
    
    day = date_string.split(" ")[1]
    day = "".join(filter(str.isdigit, day))
    # check integrity
    assert (
        year.isnumeric()
    ), f"The year is not numeric. year: {year} input: {date_string}"
    assert (
        month.isnumeric()
    ), f"The month is not numeric. month: {month} input: {date_string}"
    assert day.isnumeric(), f"The day is not numeric. day: {day} input: {date_string}"
    return year, month, day


def store_boe_pdfs(base_url, minutes_url):
    """Finds .pdf files stored at the given url and stores them within the
    repository for later analysis.
    Args:
        base_url (str): The main url for the Comptroller of Baltimore's webiste
        minutes_url (str): The url where the function can find links to pages of
            pdf files organized by year
    Returns:
        None: This is a void function.
    """
    response = requests.get(minutes_url)
    soup = BeautifulSoup(response.text, "html.parser")
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
        response_annual = requests.get(annual_url)
        soup_annual = BeautifulSoup(response_annual.text, "html.parser")
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
            if any(char.isdigit() for char in pdf_html_text):
                pdf_year, pdf_month, pdf_day = parse_long_dates(pdf_html_text)
                pdf_filename = "_".join([pdf_year, pdf_month, pdf_day]) + ".pdf"
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
        except:
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
            row = {
                "date": date,
                "page_number": page_number,
                "minutes": minutes.strip()
            }
            text_df = text_df.append(row, ignore_index=True)
        except ValueError:
            print(f"No date found for file {pdf_path}")
    print(f"Wrote {len(text_df)} rows to the table of minutes.")
    return text_df


def is_empty(_dir: Path) -> bool:
    return not bool([_ for _ in _dir.iterdir()])


def replace_chars(text):
    replacements = [('Œ', '-'),
                    ('ﬁ', '"'),
                    ('ﬂ', '"'),
                    ('™', "'"),
                    ('Ł', '•'),
                    (',', "'"),
                    ('Š', '-'),
                    ('€', ' '),
                    ('¬', '-'),
                    ('–', '…'),
                    ('‚', "'"),
                    ('Ž', '™'),
                    ('˚', 'fl'),
                    ('˜', 'fi'),
                    ('˛', 'ff'),
                    ('˝', 'ffi'),
                    ('š', '—'),
                    ('ü', 'ti'),
                    ('î', 'í'),
                    ('è', 'c'),
                    ('ë', 'e'),
                    ('Ð', '–'),
                    ('Ò', '"'),
                    ('Ó', '"'),
                    ('Õ', "'"),
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
        start_soup (BeautifulSoup object): the beautifulsoup object that parses the "landing page" for the minutes links

    Returns:
        year_links (dict): dictionary with the years (2009, 2010, ..., current year) as keys and relative links as values
    """
    # this eliminates the need to specify the years to grab since four-digit years are used consistently
    year_tags = start_soup.find_all('a', href=True, text=re.compile(r'^20\d{2}$'))  # find the tags that link to the minutes for specific years
    year_links = {tag.string: tag.get('href') for tag in year_tags}  # extracting the links

    return year_links


def month_match_lev(text):
    """
    Args: 
        text (str): the misspelled month string

    Returns:
        best_match (str): the month string that best matches the misspelled input
        best_score (int): the Levenshtein distance between text and best_match
    """
    text = text.lower()
    best_match = ''
    best_score = 9999  # lower scores are better
    for i in months:
        # lev dist == num changes to make text into i
        score = levenshtein(text, i)  
        if score < best_score:
            best_score = score
            best_match = i

    return best_match, best_score