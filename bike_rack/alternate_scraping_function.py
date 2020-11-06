import os
import requests
from bs4 import BeautifulSoup
import re

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
        if month_error in v:  # if we find a match, return the correct month
            return k
        return False  # no match found


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
    # reference: 'june'  (move this string right one character at at time)
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
    match = check_dels(word, typ_dict)
    if match:
        # print('returning from dels')
        return (match, len(match))
    else:
        # print('returning from misspells')
        return check_misspells(word)


def get_boe_minutes(base_url="https://comptroller.baltimorecity.gov",
                    minutes_url_part="/boe/meetings/minutes",
                    save_folder='BoE Minutes PDFs',
                    start_dir=os.path.dirname(__file__),
                    file_label='BoE Minutes'):
    """
    base_url:
        url for the comptrollers website

    minutes_url:
        the extra bit of the URL that specifies the minutes "landing page"

    https://comptroller.baltimorecity.gov/boe/meetings/minutes

    save_folder:
        the name of the folder used to hold the minutes PDFs,
        shouldn't have any slashes

    start_dir:
        defaults to the directory the calling script is in. used to
        make a full path (relative to the calling script or absolute)
        with save_folder
    """
    # print(start_dir)  # print the directory this script is in
    os.chdir(start_dir)  # set the cwd to avoid any OS/python shenanigans
    pdf_save_dir = f'{start_dir}/{save_folder}/'  # set save directory for pdfs
    os.makedirs(pdf_save_dir, exist_ok=True)  # create directory if it doesn't exist (no error if it does)
    minutes_url = base_url + minutes_url_part

    # alphabet is used to differentiate meetings on the same day
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
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
                  'december': '12'}

    start_page = requests.get(minutes_url)  # grab the 'starting page' that provides links to the minutes for a specific year
    start_page.raise_for_status()
    start_soup = BeautifulSoup(start_page.text, 'lxml')

    # this eliminates the need to specify the years to grab since four-digit years are used consistently
    year_tags = start_soup.find_all('a', href=True, text=re.compile(r'^20\d{2}$'))  # find the tags that link to the minutes for specific years
    year_links = [tag.get('href') for tag in year_tags]  # extracting the links
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

    for link in year_links:  # each iteration scrapes the minutes for a given year
        print(link)
        year_page = requests.get(base_url+link)
        year_page.raise_for_status()
        soup = BeautifulSoup(year_page.text, 'lxml')

        link_container_tag = soup.select("div[class='field field-name-body'] > p:last-of-type")[0]
        minutes_tags = link_container_tag.find_all('a')#, text=date_regex)  # grab tags that link to the pdfs
        link_list = list()

        for tag in minutes_tags:  # each iteration is a single minutes file
            # print(tag.text)
            file_name_re = date_regex.search(tag.text)
            # filename format: '{file_label} YYYY-MM-DD.pdf'
            # example filename: 'BoE Minutes 2009-04-01.pdf'

            if file_name_re == None:  # link with no text
                print(f'Bad link found: {tag.get("href")}, skipping')
                continue

            try:  # most links will fit this pattern
                file_name = (
                    f'{file_label} '
                    + file_name_re.group(3) # year
                    + '-'
                    + month_dict[file_name_re.group(1).lower()] # month
                    + '-'
                    + file_name_re.group(2).zfill(2) # day
                )
            except KeyError as e:  # this code only triggers if there's a typo in the month string
                month_error = file_name_re.group(1).lower()
                print(f'Error "{e}" for minutes on: "{tag.string}", '
                      f'regex found: {file_name_re.groups()}. '
                      f'Attempting typo matching...')
                correct_month, score = pick_best_month(month_error)

                try:
                    file_name = (
                        f'{file_label} '
                        + file_name_re.group(3) # year
                        + '-'
                        + month_dict[correct_month] # month
                        + '-'
                        + file_name_re.group(2).zfill(2) # day
                    )
                except:
                    #  sorry, you'll have to update the matching if you hit this code
                    print(f'Error: could not match month string '
                          f'{file_name_re.group(1)} in '
                          f'match {file_name_re.groups()}. ')
                    continue
            
            # if we find more than one meeting on a particular date, append a letter to differentiate
            temp_counter = 0
            suffix = ''
            while file_name+suffix in link_list:
                temp_counter += 1
                suffix = alphabet[temp_counter]
            link_list.append(file_name+suffix)
            file_name += suffix + '.pdf'

            if os.path.exists(pdf_save_dir + file_name):  # skip the download if we've already done it
                print(f'skipping: {file_name}')
            else:
                if tag.get('href').startswith('http'):  # because there is literally ONE link in the entire list that is an absolute path
                    min_url = tag.get('href')
                else:
                    min_url = base_url + tag.get('href')
                minutes_req = requests.get(min_url)
                minutes_req.raise_for_status()
                with open(pdf_save_dir + file_name, 'wb') as p:  # save the file
                    p.write(minutes_req.content)
                print(f'saved: {file_name}')
