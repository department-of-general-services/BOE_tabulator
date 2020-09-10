import os
import re
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
from pprint import pprint as pp
import PyPDF2

default_db_name = 'boe_minutes.db'

def regexp(term, text):
    reg = re.compile(term)
    return reg.search(text) is not None


def search(text, start_date='', end_date='', db_name=default_db_name):
    """
    text:
        some text to search for must be supplied, otherwise the function returns "None" immediately
        this text will be interpreted as a regular expression, so 
    
    start_date and end_date:
        start and end dates must be in the ISO date format (YYYY-MM-DD) Ex: '2010-06-23'
        if either start or end date is not specified (empty string) they are set the earliest or latest dates in the DB, respectively
    
    db_name:
        filename of the db. relative paths start from the directory of the calling script, otherwise an absolute path is required.
    
    return:
        returns a list of tuples, where each tuple is a row returned by the SQL command

    SQLite supports REGEXP as a matching function but does not specify one by default. The user has to add it themselves to a DB.
    SQLite _does_ support GLOB syntax by default
    See: https://www.sqlite.org/lang_expr.html#the_like_glob_regexp_and_match_operators
    """
    if text == None:
        return None
    try:
        conn = sqlite3.connect(db_name)
        if start_date == '':  # set start_date to the earliest date in the DB
            with conn:
                start_date = conn.execute("SELECT min(min_date) FROM minutes").fetchall()[0][0]
        if end_date == '':  # set end_date to the latest date in the DB
            with conn:
                end_date = conn.execute("SELECT max(min_date) FROM minutes").fetchall()[0][0]
        # print(start_date, end_date)

        with conn:
            conn.create_function('REGEXP', 2, regexp)  # this adds regex functionality but seems to have to be added every time (this seems strange, will investigate)
            return conn.execute("SELECT filename, min_text FROM minutes WHERE min_date BETWEEN ? AND ? AND min_text REGEXP ?", (start_date, end_date, text))
    except sqlite3.DatabaseError as e:
        print(f"Database error with: {db_name}.\nError: {e}")
    

def update_db(min_folder='BoE Minutes PDFs', db_name=default_db_name):
    """
    min_folder:
        folder the minutes PDFs are stored in. if the minutes folder is not in the same directory as the calling script, an absolute path is required

    db_name:
        filename of the db. relative paths start from the directory of the calling script, otherwise an absolute path is required.
    """
    os.chdir(os.path.dirname(__file__))
    pdf_date_list = list()

    for filename in os.scandir(min_folder):  # create a list of all files in the minutes folder
        pdf_date_list.append(filename.name)

    conn = sqlite3.connect(db_name)
    with conn:
        a = conn.execute("SELECT filename FROM minutes")

    ad = [i[0] for i in a.fetchall()]  # list of filenames already in the db

    for date in ad:  # remove files that are already in the db from the list of updates
        try:
            pdf_date_list.remove(date)
        except:
            pass
    pp(pdf_date_list)
    if len(pdf_date_list):  # run only if there are any updates
        min_data = create_db_row_values(file_get_list=pdf_date_list)
        # pp(len(min_data))
        with conn:  # update the db with new data
            conn.executemany("""
                INSERT INTO minutes (filename, min_date, min_text) VALUES (?, ?, ?)
            """, min_data)


def create_and_populate_minutes_db(min_folder='BoE Minutes PDFs', db_name=default_db_name):
    """
    min_folder:
        folder the minutes PDFs are stored in. if the minutes folder is not in the same directory as the calling script, an absolute path is required

    db_name:
        filename of the db. relative paths start from the directory of the calling script, otherwise an absolute path is required.

    What should the schema look like?
    one table? probably
    fields:
        id (PK, autoincrement)
        filename
        min_date (text, sqlite doesn't have a date/time data type, uses various time functions on standard datetime string formats, eg: YYYY-MM-DD)
        text (of the document)
    metadata table: ????? (probably not)
        db creation date/time
    """
    os.chdir(os.path.dirname(__file__))
    try:  # this allows this function to be called to completely recreate the db from source data if necessary
        os.remove(db_name)
    except:
        pass
    
    min_data = create_db_row_values(min_folder)
    conn = sqlite3.connect(db_name)
    with conn:  # create the table and populate the db
        conn.execute("""
            CREATE TABLE IF NOT EXISTS minutes (
                id INTEGER CONSTRAINT min_id_pk PRIMARY KEY AUTOINCREMENT, 
                filename TEXT,
                min_date TEXT,
                min_text TEXT
            )
        """)
        conn.executemany("""
            INSERT INTO minutes (filename, min_date, min_text) VALUES (?, ?, ?)
        """, min_data)


def create_db_row_values(min_folder='BoE Minutes PDFs', file_get_list=[]):
    min_data = list()
    if file_get_list == []:  # if no list specified, do all files in min_folder
        file_get_list = [i.name for i in os.scandir(min_folder)]
        print('doing scandir')
    for filename in file_get_list:
        fullpath = f'{min_folder}/{filename}'
        pdf_text = get_pdf_text(fullpath)
        min_date = filename[filename.rfind(' ')+1:-4]  # assumes that a YYYY-MM-DD date string is the end of the filename (not including the file extension)
        min_data.append((filename, min_date, pdf_text))
        # print((filename, min_date, pdf_text[:100]))
    return min_data


def get_pdf_text(fullpath, joiner='\n'):
    """
    fullpath:
        fully-qualified path (relative or absolute) to the pdf

    joiner:
        the text to use to concatenate the page texts. defaults to newline character
    """
    print(f'getting text for {fullpath}')
    replacements = [('Œ', '-'),
                    ('ﬁ', '"'),
                    ('ﬂ', '"'),
                    ('™', "'"),
                    ('Ł', '•'),
                ]
    pdf_reader = PyPDF2.PdfFileReader(fullpath)
    pdf_text = list()
    for page in pdf_reader.pages:
        pdf_text.append(page.extractText().strip())
    pdf_text = joiner.join(pdf_text)
    for i in replacements:
        pdf_text = pdf_text.replace(i[0], i[1])
    return pdf_text


def get_boe_minutes(save_folder='BoE Minutes PDFs', start_dir=os.path.dirname(__file__)):
    """
    save_folder:
        the name of the folder used to hold the minutes PDFs, shouldn't have any slashes

    start_dir:
        defaults to the directory the calling script is in. used to make a full path (relative to the calling script or absolute) with save_folder
    """
    # print(start_dir)  # print the directory this script is in
    os.chdir(start_dir)  # set the cwd to avoid any OS/python shenanigans
    pdf_save_dir = f'{start_dir}/{save_folder}/'  # set save directory for pdfs
    os.makedirs(pdf_save_dir, exist_ok=True)  # create directory if it doesn't exist (no error if it does)

    base_url = "https://comptroller.baltimorecity.gov"  # because relative hrefs
    minutes_url = base_url + "/boe/meetings/minutes"
        # https://comptroller.baltimorecity.gov/boe/meetings/minutes
    # because whoever wrote the BoE website didn't make it easy to scrape
    # date_regex = re.compile(r'([(January|February|March|April|May|June|July|August|September|October|November|December)]) (\d{1,2}), (\d{4})', re.IGNORECASE)
    date_regex = re.compile(r'(\w*)\s+(\d{1,2})\D*(\d{4})', re.IGNORECASE)
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

    # this creates a dictionary containing all possible single-letter deletions of every month
    # it's used to correct for typos in the text of a link to the minutes
    # ex: Novembe 17, 2010 (one of two real examples as of Aug 9, 2020)
    typo_dict = {k: list() for k in month_dict.keys()}
    for month in typo_dict.keys():
        for i in range(len(month)):
            typo_dict[month].append(month[:i] + month[i+1:])

    start_page = requests.get(minutes_url)  # grab the 'starting page' that provides links to the minutes for a specific year
    start_page.raise_for_status()  # doing the \
    start_soup = BS(start_page.text, 'lxml')  # needful

    # this eliminates the need to specify the years to grab since four-digit years are used consistently
    year_tags = start_soup.find_all('a', href=True, text=re.compile(r'^\d{4}$'))  # find the tags that link to the minutes for specific years
    year_links = [tag.get('href') for tag in year_tags]  # extracting the links

    for link in year_links:
        print(link)
        year_page = requests.get(link)
        year_page.raise_for_status()
        soup = BS(year_page.text, 'lxml')

        minutes_tags = soup.find_all('a', text=date_regex)  # grab tags that link to the pdfs

        for tag in minutes_tags:
            file_name_re = date_regex.search(tag.string)
            # example filename: 'BoE Minutes 2009-04-01.pdf'

            try:  # most links will fit this pattern
                file_name = 'BoE Minutes ' + file_name_re.group(3) + '-' + month_dict[file_name_re.group(1).lower()] + '-' + file_name_re.group(2).zfill(2) + '.pdf'
            except KeyError as e:  # this code only triggers if there's a typo in the month string
                month_error = file_name_re.group(1).lower()
                print(f'Error "{e}" for minutes on: "{tag.string}", regex found: {file_name_re.groups()}. Attempting typo matching...')
                for k, v in typo_dict.items():  # this loop searches for matches among single-letter deletions
                    correct_month = False
                    if month_error in v:
                        correct_month = k
                        break

                if correct_month:  # if we found a match
                    file_name = 'BoE Minutes ' + file_name_re.group(3) + '-' + month_dict[correct_month] + '-' + file_name_re.group(2).zfill(2) + '.pdf'
                else:
                    #  sorry, you'll have to update the regex if you hit this code
                    print(f'Error: could not match month string {file_name_re.group(1)} in match {file_name_re.groups()}. ')

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


if __name__ == '__main__':

    get_boe_minutes()
    create_and_populate_minutes_db()
    # update_db()
    search_term = 'Sheila Dixon'
    # print('after regexp')
    results = search(search_term)

    if results is not None:
        for result in results.fetchall():  # print the filename
            term_index = result[1].find(search_term)
            print(result[0]+'\n', result[1][term_index-100:term_index+100])
            print('-'*30)