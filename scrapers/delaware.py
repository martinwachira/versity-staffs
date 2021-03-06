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

def delaware_scraper(name):
    print('Retrieving ' + name + "'s email...")
    first_name, last_name = split_name(name)
    cache = Cache()
    try:
        email = cache[name]
        return email
    except KeyError:
        pass
    query_link = DIRECTORIES.get('delaware')
    driver = get_driver()
    driver.get(query_link)
    driver.implicitly_wait(5)
    driver.find_element_by_id('lastName').send_keys(
        last_name)
    driver.find_element_by_id('firstName').send_keys(
        first_name)
    driver.find_element_by_css_selector('form button[type="submit"]').click()
    driver.implicitly_wait(5)
    time.sleep(3)
    try:
        email = driver.find_element_by_xpath('//div[contains(@role, "main")]//a[contains(@href, "mailto")]')
        email = email.text
        print(email)
    except selenium.common.exceptions.NoSuchElementException:
        email = None
    driver.quit()
    email = email if email else None
    cache[name] = email
    return email
