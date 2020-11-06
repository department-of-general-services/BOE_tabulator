import requests
from bs4 import BeautifulSoup

def check_page_setup(url):
    response = requests.get(url)
    checks = {'request': 'fail'}

    # checks if request went through successfully
    if response.status_code == 200:
        checks['request'] = 'pass'
    else:
        checks['error_message'] = response.reason
        return checks

    # if all checks pass set error message to none and return checks

    checks['error_message'] = None
    return checks
