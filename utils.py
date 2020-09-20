import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from pathlib import Path
import re
import PyPDF2
from datetime import datetime
from pathlib import Path


def check_dels(month_error, typ_dict):
    """
    Checks a dictionary of single-letter deletions of the months for a match

    Args:
        month_error (str): the month string with a typo (long months,
            e.g., "Novembe")
        typo_dict (dict): dictionary with months for keys, values are lists
            of all single-letter deletions for that month (key)

    Returns:
        returns the correct month string if a match is found, otherwise it
            returns False
    """
    for k, v in typ_dict.items():
        correct_month = False  # set return value for not finding a match
        if month_error in v:  # if we find a match, return the correct month
            return k


def sliding_window(test, reference):
    """
    Uses a sliding window method to try to find the best match for a misspelled
        month. Imagine a transparent reference window printed with the target
        string on it. This window is slid across the test string and each
        position is checked for how similar it is to the reference. This score
        is used to determine the most likely "correct" substring in the test.
        More detailed explanation here:
            https://www.geeksforgeeks.org/window-sliding-technique/

    Args:
        test (str): the (potentially) misspelled string that needs correcting
        reference (str): the target string we're comparing the test string to

    Returns:
        tuple(best_match, best_match_score)
            best_match (str): methods best guess at what the correct month is
            best_match_score (int): numeric score for how good the match is
                higher is better, can be normalized to len(month)
    """
    best_score = 0
    best_result = ''
    ref_len = len(reference)
    # padding the string to avoid out of bounds errors and allow head-to-tail
    #  comparisons. For example:
    # reference: 'june'  (move this string right one character at at ime)
    # test:      '    une    '
    test = (ref_len*' ') + test + (ref_len*' ')

    for i in range(len(test)-ref_len):  # iterate through all indices
        score = score_window(test[i:i+ref_len], reference)
        if best_score < score:
            best_score = score
            best_result = test[i:i+ref_len]

    return (best_result, best_score)


def score_window(window, target):
    """
    Compare the data in the window to the target sequence
        and compute a numeric score based on how similar it is

    Args:
        window (str): a substring of equal length to target, from the test
            string in sliding_window
        target (str): the sequence we're looking for
    """
    score = 0
    if len(window) != len(target):
        # print('unequal')
        return -1  # unequal lengths don't work with this method
    for i in range(len(window)):  # iterate letter-by-letter
        if window[i] == target[i]:
            score += 1  # matches increase score, higher scores are better
    return score


def check_misspells(word):
    """
    'Wrapper' function for sliding_window that compares a (potentially)
        misspelled word (word) to each of the months to find the best match

    Args:
        word (str): the misspelled month string
    Returns:
        tuple(best_match, best_match_score)
            best_match (str): methods best guess at what the correct month is
            best_match_score (int): numeric score for how good the match is
                higher is better, can be normalized to len(month)
    """
    months = [
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
        'december']
    best_score = 0
    best_result = ''
    for month in months:
        if abs(len(month) - len(word)) > 1:
            continue
        result, score = sliding_window(word, month)
        # print(result, score)
        if score > best_score:
            best_score = score
            best_result = month
    return (best_result, best_score)


def make_typo_dict(word_list=[]):
    """
    Creates a dictionary with keys equal to word_list, with values being a 
        list of every possible single-letter deletion of that word

    Args:
        word_list (list): a list of strings to make single deletions from. If
            none is provided (i.e., an empty list) is uses the keys from the
            month_dict below.
    Returns:
        typo_dict (dict): dictionary containing every possible single-letter
            deletion of each of the keys in the dict    
    """
    month_dict = {'january': '01',
                  'february': '02',
                  'march': '03',
                  'april': '04',
                  'may': '05',
                  'june': '06',
                  'july': '07',
                  'august': '08',
                  'september': '09',
                  'october': '10',
                  'november': '11',
                  'december': '12'
                }
    if len(word_list) == 0:
        word_list = month_dict.keys()

    # this creates a dictionary containing all possible single-letter deletions of every month
    # it's used to correct for typos in the text of a link to the minutes
    # ex: Novembe 17, 2010 (one of two real examples as of Aug 9, 2020)
    typo_dict = {k: list() for k in word_list}
    for month in typo_dict.keys():
        for i in range(len(month)):
            typo_dict[month].append(month[:i] + month[i+1:])
    
    return typo_dict


def pick_best_month(word, typ_dict=make_typo_dict()):
    """
    'Wrapper' function for various spell-checking methods. Check deletions
        first to avoid known errors with deletions and sliding_window.

    Args:
        word (str): the misspelled month string
        typo_dict (dict): dictionary with months for keys, values are lists
            of all single-letter deletions for that month (key)

    Returns:
        tuple(best_match, best_match_score)
            best_match (str): methods best guess at what the correct month is
            best_match_score (int): numeric score for how good the match is
                higher is better, can be normalized to len(month)
    """
    # returns a tuple (best match, match score)
    if match := check_dels(word, typ_dict):
        # print('returning from dels')
        return (match, len(match))
    else:
        # print('returning from misspells')
        return check_misspells(word)


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
            row = {"date": date, "page_number": page_number, "minutes": minutes.strip()}
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
