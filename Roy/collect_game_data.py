import requests
import Roy.config as config
from bs4 import BeautifulSoup
import regex as re
import datetime
import json


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
        if key not in config.relevant_keys:
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


if __name__ == '__main__':
    page = requests.get(config.divinity_game_example)

    soup = BeautifulSoup(page.content)
    # print(soup.prettify())

    #game sku
    game_sku = int(soup.find(class_="layout").attrs["card-product"])

    # Game name
    game_title = soup.find('h1').text
    game_score = float(soup.find(class_="rating productcard-rating__score").text[:3])
    # Prices
    game_price_base = float(soup.find("span", {"class": "product-actions-price__base-amount _price"}).text)
    game_price_final = float(soup.find("span", {"class": "product-actions-price__final-amount _price"}).text)
    game_price_discount = round((float(game_price_base) - float(game_price_final)) / float(game_price_base), 2)
    # Game details
    game_details_dict = game_details(soup)
    print(game_sku, game_title, game_score, game_price_base, game_price_final, game_price_discount, game_details_dict)