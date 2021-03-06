from lxml.html import fromstring
import requests
from urllib.parse import urljoin, urlparse
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import selenium

from url_downloader import get_driver
from utils import DIRECTORIES, split_name
from cache import Cache


def temple_scraper(name):
    print('Retrieving ' + name + "'s email...")
    cache = Cache()
    try:
        email = cache[name]
        return email
    except KeyError:
        pass
    first_name, last_name = split_name(name)
    query_link = DIRECTORIES.get('temple')
    driver = get_driver()
    driver.delete_all_cookies()
    driver.get(query_link)
    driver.implicitly_wait(5)
    driver.find_element_by_id('templeedusn').send_keys(
        last_name)
    driver.find_element_by_id('templeedugivenname').send_keys(
        first_name)
    driver.find_element_by_css_selector('form input.Search').click()
    driver.implicitly_wait(3)
    try:
        email = driver.find_element_by_xpath('//div[contains(@id, "Div_Column_02")]//a[contains(@href, "mailto")]')
        email = email.text
        print(email)
    except selenium.common.exceptions.NoSuchElementException:
        email = None
    driver.delete_all_cookies()
    driver.quit()
    if email is not None:
        cache[name] = email
    return email
