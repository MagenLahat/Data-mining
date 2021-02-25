# TODO: HEADLINE
""""""
import config
import re
import datetime


def __clean_key(key):
    """Cleans the field name.
     That key need to be the field name in the sql"""
    try:
        key_cleaner = str(key)
        key_cleaner = key_cleaner.lower()
        key_cleaner = re.sub(r'[:]', '', key_cleaner.strip())
        if re.match(r'\w+ \w+', key_cleaner):
            # adding underscore between two words (for SQL columns' names)
            key_cleaner = re.sub(' ', '_', key_cleaner)
    except:
        return "NULL"
    return key_cleaner


#  Game Details
def __game_genre_cleaner(row):
    """Returns the game genre"""
    new_line_regex = r'[\n]'
    try:
        game_genre = row.text.strip()
        game_genre = re.sub(new_line_regex, '', game_genre)
        game_genre = game_genre.split(' - ')
        for idx, game in enumerate(game_genre):
            game_genre[idx] = game.strip()
    except:
        return "NULL"
    return game_genre


def __works_on_cleaner(row):
    """Returns on which OSs' the game is working"""
    try:
        works_on = row.text.lower().strip()
    except:
        return 'NULL'
    return works_on


def __release_date_cleaner(row):
    """Returns the game's release date YYYY-mm-dd (datetime)"""
    datetime_regex = r'\d{4}-\d{2}-\d{2}'
    try:
        release_date = re.search(datetime_regex, row.text).group()
        release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
    except:
        return "NULL"
    return release_date


def __game_developers_cleaner(row):
    """Returns the game's developers & publisher names (list)"""
    try:
        company = row.text.lower()
        company = re.sub(r'[\n]', '', company)
        company = company.split(r'/')
        for idx, comp in enumerate(company):
            company[idx] = comp.strip()
    except:
        return ['NULL']
    return company


def size_cleaner_and_converter(row):
    """Returns the size of the game in MB(float)"""
    to_mb_scale = 1000
    try:
        size = row.text.lower()
        size = re.sub(r'[\n]', '', size)
        size = size.strip()
        size_digits = float(size[:size.find(' ')])
        size_scale = size[size.find(' ')+1:]
        if size_scale == 'gb':
            size_digits *= to_mb_scale
        elif size_scale == 'kb':
            size_digits /= to_mb_scale
    except:
        return "NULL"
    return size_digits


def game_details(soup):
    """Calling the other functions (above)
     in order to parse and clean the Game details section
     Returns: game_details_section (dictionary)
     """
    game_details_section = dict()
    for row in soup.find_all("div", {"class": "details__content table__row-content"}):
        key = __clean_key(row.previous_element)
        if key not in config.relevant_keys:
            continue
        if key == 'genre':
            value = __game_genre_cleaner(row)
        elif key == 'works_on':
            value = __works_on_cleaner(row)
        elif key == 'release_date':
            value = __release_date_cleaner(row)
        elif key == 'company':
            value = __game_developers_cleaner(row)
        elif key == 'size':
            value = size_cleaner_and_converter(row)
        game_details_section[key] = value
    return game_details_section