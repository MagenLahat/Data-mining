import requests
import config as conf
from bs4 import BeautifulSoup
import regex as re
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import os


def clean_key(key):
    """Cleans the key of the dict. That key need to be the field name in the sql"""
    key_cleaner = str(key)
    key_cleaner = key_cleaner.lower()
    key_cleaner = re.sub(r'[:]', '', key_cleaner.strip())
    if re.match(r'\w+ \w+', key_cleaner):
        key_cleaner = re.sub(' ','_',key_cleaner)
    return key_cleaner


#  Game Details
def game_gnere_cleaner(row):
    """returns the game gneres lowercase"""
    game_gnere = row.text.strip()
    game_gnere = re.sub(r'[\n]', '', game_gnere)
    game_gnere = game_gnere.split(' - ')
    for idx, game in enumerate(game_gnere):
        game_gnere[idx] = game.strip()
    return game_gnere

def works_on_cleaner(row):
    """Operating system cleaner"""
    works_on = row.text.lower().strip()
    return works_on


def release_date_cleaner(row):
    """Returns game release date"""
    release_date = re.search(r'\d{4}-\d{2}-\d{2}', row.text).group()
    release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
    return release_date


def company_cleaner(row):
    company = row.text.lower()
    company = re.sub(r'[\n]', '', company)
    company = company.split(r'/')
    for idx, comp in enumerate(company):
        company[idx] = comp.strip()
    return company


def size_cleaner_and_converter(row):
    """Returns the size of the game in MB(float)"""
    size = row.text.lower()
    size = re.sub(r'[\n]', '', size)
    size = size.strip()
    size_digits = float(size[:size.find(' ')])
    size_scale = size[size.find(' ')+1:]
    if size_scale == 'gb':
        size_digits *= 1000
    elif size_scale == 'kb':
        size_digits /= 1000
    return size_digits

# aaa_rows = soup.find_all("div", {"class": "details__content table__row-content"})


def game_details(soup):
    """Calling other functions in order to parse and clean Game details data"""
    array = dict()
    for row in soup.find_all("div", {"class": "details__content table__row-content"}):
        key = clean_key(row.previous_element)
        if key not in conf.relevant_keys:
            continue
        if key == 'genre':
            value = game_gnere_cleaner(row)
        elif key == 'works_on':
            value = works_on_cleaner(row)
        elif key == 'release_date':
            value = release_date_cleaner(row)
        elif key == 'company':
            value = company_cleaner(row)
        elif key == 'size':
            value = size_cleaner_and_converter(row)
        array[key] = value
    return array


def game_sku(soup):
    """Returns the game SKU else returns null"""
    # game sku
    game_sku = int(soup.find(class_="layout").attrs["card-product"])
    if game_sku is None:
        return 'NULL'
    return game_sku


def game_title(soup):
    """Returns the game title else returns null"""
    game_title = soup.find('h1').text
    if game_title is None:
        return 'NULL'
    return game_title


def game_score(soup):
    """Returns the game score of of 5 (highest)"""
    try:
        game_score = soup.find(class_="rating productcard-rating__score").text
        game_score = float(re.search(r'(\d{1}\.?\d?)/', game_score).group().replace(r'/',''))
    except AttributeError:
        return 'NULL'
    return game_score


def game_price_base(soup):
    """Returns the game prices"""
    game_price_base = float(soup.find("span", {"class": "product-actions-price__base-amount _price"}).text)
    if game_price_base is None:
        return "NULL"
    return game_price_base


def game_price_final(soup):
    """Returns the game prices"""
    game_price_final = float(soup.find("span", {"class": "product-actions-price__final-amount _price"}).text)
    if game_price_final is None:
        return "NULL"
    return game_price_final


def game_price_discount(game_price_base, game_price_final):
    """Returns the discount of the game. If no discount returns zero"""
    no_discount = 0
    if game_price_base == game_price_final or game_price_base == 'NULL' or game_price_final == 'NULL':
        return no_discount
    else:
        return round((float(game_price_base) - float(game_price_final)) / float(game_price_base), 2)


def master_page_scrapper(page):
    soup = BeautifulSoup(page.content, features="lxml")
    game_sql = {} # The data of the game
    game_sql['game_sku'] = game_sku(soup)
    game_sql['game_title'] = game_title(soup)
    game_sql['game_score'] = game_score(soup)
    game_sql['game_price_base'] = game_price_base(soup)
    game_sql['game_price_final'] = game_price_final(soup)
    game_sql['game_price_discount'] = game_price_discount(game_sql['game_price_base'], game_sql['game_price_final'])
    # Game details
    game_details_dict = game_details(soup)
    game_sql['game_url'] = page.url
    game_sql = {**game_sql, **game_details_dict}
    return game_sql


def get_pages():
    driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
    index = 1
    game_urls = []
    while index:
        # todo: remove after finish
        # if index == 2:
        #     break

        driver.get(conf.gog_url_partial + str(index))
        if index > 1 and driver.current_url == conf.gog_url:  # if it returns to the first page finish
            break
        try:
            element = WebDriverWait(driver, 10).until(  # wait until the element is loaded
                EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            # common selenium exception for items that were not loaded on time
            elems = driver.find_elements_by_tag_name('a')
            # sleep(10)
            for elem in elems:
                href = elem.get_attribute('href')
                if href is not None and href.startswith("https://www.gog.com/game/"):
                    print(href) #todo: delete after we finish
                    game_urls.append(href)
            index += 1
        except StaleElementReferenceException:
            print(f'stale element reference raised for page {index}, skipping page...')
            sleep(10)
            index += 1

        except ConnectionRefusedError:
            print(f'connection refused error raised {index}, skipping page...')
            sleep(10)
            index += 1
    driver.quit()
    return game_urls


if __name__ == '__main__':

    for page in get_pages():
    # for page in ["https://www.gog.com/game/new_super_luckys_tale"]:
        rs = requests.get(page)

        game_data = master_page_scrapper(rs)

        print(game_data)




