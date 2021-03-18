"""
Project: Data-Mining GOG (Good Old Games)
Sub-file of game_scrapper.py
Retrieve Data from game page url
"""
import re
import config


def __game_sku(soup):
    """Returns the game's SKU (int)"""
    # game sku
    try:
        game_sku = int(soup.find(class_=config.game_sku_find_class).attrs[config.game_sku_find_attr])
    except Exception:
        # if game_sku is None
        return config.NULL_VALUE
    return game_sku


def __game_title(soup):
    """Returns the game's Title
    Game Title is a MUST field.
    Handling null in "game_master_scrapper"
    function
    """
    try:
        game_title = soup.find(config.game_title_find_tag).text
    except Exception:
        # if game_title is None
        return config.NULL_VALUE
    return game_title


def __game_score(soup):
    """Returns the game score of of 5 (highest)"""
    try:
        game_score = soup.find(class_=config.game_score_find_class).text
        game_score = float(
            re.search(config.game_score_search_regex, game_score).group().replace(config.game_score_regex_slash,
                                                                                  config.EMPTY_STRING))
    except AttributeError:
        return config.NULL_VALUE
    return game_score


def __game_price_base(soup):
    """Returns the game base price (before discount) (float)"""
    try:
        game_price_base = float(soup.find(config.SPAN_TAG,
                                          {config.CLASS_TAG: config.game_price_base_text}).text)
    except:
        # if game_price_base is None
        return config.NULL_VALUE
    return game_price_base


def __game_price_final(soup):
    """Returns the game final price (after discount) (float)"""
    try:
        game_price_final = float(soup.find(config.SPAN_TAG,
                                           {config.CLASS_TAG: config.game_price_final_text}).text)
    except:
        return config.NULL_VALUE
    return game_price_final


def __game_price_discount(game_price_base, game_price_final):
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


def game_data(game_page_url, soup):
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
    game_data_dict[config.keyname_game_title] = __game_title(soup)
    if game_data_dict[config.keyname_game_title] == config.NULL_VALUE:
        raise ValueError(config.no_game_title_error_message)
    # rest of keynames
    game_data_dict[config.keyname_game_sku] = __game_sku(soup)
    game_data_dict[config.keyname_game_score] = __game_score(soup)
    game_data_dict[config.keyname_game_base_price] = __game_price_base(soup)
    game_data_dict[config.keyname_gmae_final_price] = __game_price_final(soup)
    game_data_dict[config.keyname_game_discount] = __game_price_discount(game_data_dict[config.keyname_game_base_price],
                                                                         game_data_dict[config.keyname_gmae_final_price])
    game_data_dict[config.keyname_game_url] = game_page_url.url
    return game_data_dict
