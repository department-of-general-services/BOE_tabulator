import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from pathlib import Path
import re
import PyPDF2
from datetime import datetime
from pathlib import Path


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
    # check for garbage at the end of the string
    while not date_string[-1].isnumeric():
        date_string = date_string[:-1]
    # grab the front of the string, where we expect the three-letter month to be
    month = date_string[:3]
    # this error will come up, so we catch it
    if month == "une":
        month = "Jun"
    # grab the back of the string to get the year
    year = date_string[-4:]
    # try to convert the month to str(int) form, or throw an error
    try:
        month = str(time.strptime(month, "%b").tm_mon)
    except ValueError as err:
        print(f"month: {month}")
        print(f"Encountered ValueError on file: {date_string}")
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

    for year in range(2009, 2021):
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


def replace_chars(val):
    val = " ".join(val.split())
    val = val.replace("™", "'")
    val = val.replace("Œ", "-")
    return val
