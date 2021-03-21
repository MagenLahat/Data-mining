"""
Project: Data-Mining GOG (Good Old Games)
Sub-file of game_scrapper.py
Retrieve Additional Details (different section on the game page)
"""
import config
import re
import datetime


def __clean_key(key):
    """Cleans the field name.
     That key need to be the field name in the sql"""
    try:
        key_cleaner = str(key)
        key_cleaner = key_cleaner.lower()
        key_cleaner = re.sub(config.PUNCTUATION_MARK, config.EMPTY_STRING, key_cleaner.strip())
        if re.match(config.WORD_REGEX, key_cleaner):
            # adding underscore between two words (for SQL columns' names)
            key_cleaner = re.sub(config.SPACE_STRING, config.UNDERLINE, key_cleaner)
    except:
        return config.NULL_VALUE
    return key_cleaner


#  Game Details
def __get_game_genre(row):
    """Returns the game genre"""
    try:
        game_genre = row.text.strip()
        game_genre = re.sub(config.NEW_LINE, config.EMPTY_STRING, game_genre)
        game_genre = game_genre.split(config.LINE_SPACED)
        for idx, game in enumerate(game_genre):
            game_genre[idx] = game.strip()
    except:
        return config.NULL_VALUE
    return game_genre


def __get_game_supported_os(row):
    """Returns on which OSs' the game is working"""
    try:
        works_on = row.text.lower().strip()
    except:
        return config.NULL_VALUE
    return works_on


def __get_game_release_date(row):
    """Returns the game's release date YYYY-mm-dd (datetime)"""
    try:
        release_date = re.search(config.DATETIME_REGEX, row.text).group()
        release_date = datetime.datetime.strptime(release_date, config.DATE_FORMAT)
    except:
        return config.NULL_VALUE
    return release_date


def __get_game_publisher(row):
    """Returns the game's developers & publisher names (list)"""
    try:
        company = row.text.lower()
        company = re.sub(config.NEW_LINE, config.EMPTY_STRING, company)
        company = company.split(config.SLASH_STRING)
        for idx, comp in enumerate(company):
            company[idx] = comp.strip()
    except:
        return [config.NULL_VALUE]
    return company


def __get_game_size_in_mb(row):
    """Returns the game_size_original of the game in MB(float)"""
    try:
        game_size_original = row.text.lower()
        game_size_original = re.sub(config.NEW_LINE, config.EMPTY_STRING, game_size_original)
        game_size_original = game_size_original.strip()
        game_size_converted = float(game_size_original[:game_size_original.find(config.SPACE_STRING)])
        size_scale = game_size_original[game_size_original.find(' ') + 1:]
        if size_scale == config.GAME_IN_GB_SIZE:
            game_size_converted *= config.TO_MB_SCALE
        elif size_scale == config.GAME_IN_KB_SIZE:
            game_size_converted /= config.TO_MB_SCALE
    except:
        return config.NULL_VALUE
    return game_size_converted


def get_game_details(soup):
    """Calling the other functions (above)
     in order to parse and clean the Game details section
     Returns: game_details_section (dictionary)
     """
    game_details_section = {key_index: config.NULL_VALUE for key_index in config.GAME_KEYS}  # Create dict with None values.
    for row in soup.find_all(config.DIV_TAG, {config.CLASS_TAG: config.game_details_text}):
        key = __clean_key(row.previous_element)
        if key not in config.GAME_KEYS:
            continue
        if key == config.KEYNAME_GENRE:
            value = __get_game_genre(row)
        elif key == config.KEYNAME_WORKS_ON:
            value = __get_game_supported_os(row)
        elif key == config.KEYNAME_RELEASE_DATE:
            value = __get_game_release_date(row)
        elif key == config.KEYNAME_COMPANY:
            value = __get_game_publisher(row)
        elif key == config.KEYNAME_GAME_SIZE:
            value = __get_game_size_in_mb(row)
        game_details_section[key] = value
    return game_details_section