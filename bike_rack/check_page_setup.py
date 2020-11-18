import requests
from bs4 import BeautifulSoup

def check_and_parse_page(url):
    response = requests.get(url)
    checks = {'pass': [],
              'fail': []}

    # checks if request went through successfully
    if response.status_code == 200:
        checks['pass'].append('request')
    else:
        checks['fail'].append('request')
        checks['error_message'] = response.reason
        return checks, None

    # tries to parse HTML from response text
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        checks['pass'].append('html_parsing')
    except:
        checks['error_message'] = 'Issue with parsing'
        return checks, None

    # if all checks pass set error message to none and return checks
    checks['error_message'] = None
    return checks, soup
