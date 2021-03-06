from lxml.html import fromstring
import requests
from urllib.parse import urljoin, urlparse
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium

from url_downloader import get_driver
from utils import DIRECTORIES
from cache import Cache

def minnesota_scraper(name):
    print('Retrieving ' + name + "'s email...")
    query_link = DIRECTORIES.get('minnesota')
    name = name.replace(" ", "+")
    cache = Cache()
    try:
        email = cache[name]
        return email
    except KeyError:
        pass
    query_link = query_link.format(name)
    driver = get_driver()
    driver.get(query_link)
    driver.implicitly_wait(5)
    time.sleep(3)
    tree = fromstring(driver.page_source)
    email = tree.xpath('//table[contains(@class, "result__single-person")]//a[contains(@href, "mailto")]/text()')
    print(email)
    driver.quit()
    email = email[0] if email else None
    if email is not None:
        cache[name] = email
    return email
