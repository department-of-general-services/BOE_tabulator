import os

def get_boe_minutes(base_url="https://comptroller.baltimorecity.gov",
                    minutes_url_part="/boe/meetings/minutes",
                    save_folder='BoE Minutes PDFs',
                    start_dir=os.path.dirname(__file__)):
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

    # because whoever wrote the BoE website didn't make it easy to scrape
    # date_regex = re.compile(r'([(January|February|March|April|May|June|July|August|September|October|November|December)]) (\d{1,2}), (\d{4})', re.IGNORECASE)
    date_regex = re.compile(r'(\w*)\s+(\d{1,2})\D*(\d{4})', re.IGNORECASE)
    """
    This regex captures any long date formats

    The compoents of the regex:
        (\w*) - First capture group, one or more word chars to find month
        \s - Space between month and date, not captured
        (\d{1,2}) - Second capture group, one or two numbers to find date
        \D* - Non decimal chars between date and year, not captured
        (\d{4}) - Third capture group, string of four numbers to find year
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
                  'december': '12'}

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
                file_name = (
                    'BoE Minutes '
                    + file_name_re.group(3) # year
                    + '-'
                    + month_dict[file_name_re.group(1).lower()] # month
                    + '-'
                    + file_name_re.group(2).zfill(2) # day
                    + '.pdf'
                )
            except KeyError as e:  # this code only triggers if there's a typo in the month string
                month_error = file_name_re.group(1).lower()
                print(f'Error "{e}" for minutes on: "{tag.string}", '
                      f'regex found: {file_name_re.groups()}. '
                      f'Attempting typo matching...')
                for k, v in typo_dict.items():  # this loop searches for matches among single-letter deletions
                    correct_month = False
                    if month_error in v:
                        correct_month = k
                        break

                if correct_month:  # if we found a match
                    file_name = (
                        'BoE Minutes '
                        + file_name_re.group(3) # year
                        + '-'
                        + month_dict[correct_month] # month
                        + '-'
                        + file_name_re.group(2).zfill(2) # day
                        + '.pdf'
                    )
                else:
                    #  sorry, you'll have to update the regex if you hit this code
                    print(f'Error: could not match month string '
                          f'{file_name_re.group(1)} in '
                          f'match {file_name_re.groups()}. ')

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
