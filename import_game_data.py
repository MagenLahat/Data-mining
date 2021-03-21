"""
Project: Data-Mining GOG (Good Old Games)
Sub-file of game_scrapper.py
Retrieve Data from game page url
"""
import re
import config


def __get_game_sku(soup):
    """Returns the game's SKU (int)"""
    # game sku
    try:
        game_sku = int(soup.find(class_=config.GAME_SKU_FIND_CLASS).attrs[config.GAME_SKU_FIND_ATTR])
    except Exception:
        # if game_sku is None
        return config.NULL_VALUE
    return game_sku


def __get_game_title(soup):
    """Returns the game's Title
    Game Title is a MUST field.
    Handling null in "game_master_scrapper"
    function
    """
    try:
        game_title = soup.find(config.GAME_TITLE_FIND_TAG).text
    except Exception:
        # if game_title is None
        return config.NULL_VALUE
    return game_title


def __get_game_score(soup):
    """Returns the game score of of 5 (highest)"""
    try:
        game_score = soup.find(class_=config.GAME_SCORE_FIND_CLASS).text
        game_score = float(
            re.search(config.GAME_SCORE_SEARCH_REGEX, game_score).group().replace(config.GAME_SCORE_REGEX_SLASH,
                                                                                  config.EMPTY_STRING))
    except AttributeError:
        return config.NULL_VALUE
    return game_score


def __get_game_price_base(soup):
    """Returns the game base price (before discount) (float)"""
    try:
        game_price_base = float(soup.find(config.SPAN_TAG,
                                          {config.CLASS_TAG: config.GAME_PRICE_BASE_TEXT}).text)
    except:
        # if game_price_base is None
        return config.NULL_VALUE
    return game_price_base


def __get_game_price_final(soup):
    """Returns the game final price (after discount) (float)"""
    try:
        game_price_final = float(soup.find(config.SPAN_TAG,
                                           {config.CLASS_TAG: config.GAME_PRICE_FINAL_TEXT}).text)
    except:
        return config.NULL_VALUE
    return game_price_final


def __get_game_price_discount(game_price_base: float, game_price_final: float):
    """Returns the discount (float) of the game. If no discount returns zero"""
    discount_percentage = 0.00

    if game_price_base == game_price_final or \
            game_price_base == config.NULL_VALUE or \
            game_price_final == config.NULL_VALUE:
        return discount_percentage
    else:
        return round((float(game_price_base) - float(game_price_final)) / float(game_price_base), 2)


def __check_game_page_url_response(game_page_url):
    """Verify game page url response"""
    if game_page_url.status_code != config.URL_GOOD_RESPONSE:
        return False
    else:
        return True


def get_game_data(game_page_url, soup):
    """ Game data - The function controls the whole file
        and responsible for the download of particular game data.
        Each sub-function handle with other part of the game page url.
        For example: __game_title retrieve the the title of the game.
        Input Vars:
        game_page_url (str) - full url of the specific game.
        soup (BeautifulSoup obj) - scrapped html object of the specific url.
    """
    game_data_dict = {}  # The data of the game

    if not __check_game_page_url_response(game_page_url):
        raise ConnectionError(f"URL Response fail{game_page_url}")

    # game title
    game_data_dict[config.KEYNAME_GAME_TITLE] = __get_game_title(soup)
    if game_data_dict[config.KEYNAME_GAME_TITLE] == config.NULL_VALUE:
        raise ValueError(config.NO_GAME_TITLE_ERROR_MESSAGE)
    # rest of keynames
    game_data_dict[config.KEYNAME_GAME_SKU] = __get_game_sku(soup)
    game_data_dict[config.KEYNAME_GAME_SCORE] = __get_game_score(soup)
    game_data_dict[config.KEYNAME_GAME_BASE_PRICE] = __get_game_price_base(soup)
    game_data_dict[config.KEYNAME_GMAE_FINAL_PRICE] = __get_game_price_final(soup)
    game_data_dict[config.KEYNAME_GAME_DISCOUNT] = __get_game_price_discount(
        game_data_dict[config.KEYNAME_GAME_BASE_PRICE], game_data_dict[config.KEYNAME_GMAE_FINAL_PRICE])
    game_data_dict[config.KEYNAME_GAME_URL] = game_page_url.url
    return game_data_dict
