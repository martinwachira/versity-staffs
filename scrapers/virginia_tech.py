from lxml.html import fromstring
import requests
from urllib.parse import urljoin, urlparse
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from url_downloader import get_driver
from utils import DIRECTORIES
from cache import Cache

def virginia_tech_scraper(name):
    print('Retrieving ' + name + "'s email...")
    cache = Cache()
    try:
        email = cache[name]
        return email
    except KeyError:
        pass
    query_link = DIRECTORIES.get('virginia tech')
    driver = get_driver()
    driver.get(query_link)
    driver.implicitly_wait(5)
    time.sleep(3)
    driver.find_element_by_id('vt_search_box').send_keys(
        name + Keys.RETURN)
    # pg_loaded = WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.ClassName, "results")))
    time.sleep(2)
    driver.implicitly_wait(5)
    #driver.find_element_by_id('people-label').click()
    tree = fromstring(driver.page_source)
    persons = tree.xpath('//div[@id="results"]//div[contains(@class, "vt-person")]')
    for person in persons:
        vt_name = person.xpath('//a[@class="vt-c-name"]/text()')
        if vt_name and all([n in vt_name[0].lower() for n in name.lower().split(' ')]):
            email = person.xpath('//li[@class="vt-cl-email"]/a/text()')
            print(email)
            print()
            break
        else:
            email = None
    time.sleep(2)
    driver.quit()
    email = email[0] if email else None
    if email is not None:
        cache[name] = email
    return email
