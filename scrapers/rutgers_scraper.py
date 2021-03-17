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
from utils import DIRECTORIES
from cache import Cache

def rutgers_scraper(name):
    print('Retrieving ' + name + "'s email...")
    cache = Cache()
    try:
        email = cache[name]
        return email
    except KeyError:
        pass
    query_link = DIRECTORIES.get('rutgers')
    driver = get_driver()
    driver.get(query_link)
    driver.implicitly_wait(5)
    driver.find_element_by_id('q').send_keys(
        name + Keys.RETURN)
    wait(driver, 30).until(
        EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name(
            "iframe")
        ))
    time.sleep(3)
    try:
        email = driver.find_element_by_xpath('//div[contains(@id, "content")]//dd//a[contains(@href, "mailto")]')
        email = email.text
        print(email)
    except selenium.common.exceptions.NoSuchElementException:
        email = None
    driver.quit()
    email = email[0] if email else None
    if email is not None:
        cache[name] = email
    return email
