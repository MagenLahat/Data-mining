# TODO: HEADLINE
""""""
import regex as re
import config


def __game_sku(soup):
    """Returns the game's SKU"""
    # game sku
    try:
        game_sku = int(soup.find(class_="layout").attrs["card-product"])
    except:
    # if game_sku is None
        return 'NULL'
    return game_sku


def __game_title(soup):
    """Returns the game's Title
    Game Title is a MUST field.
    Handling null in "game_master_scrapper"
    function
    """
    try:
        game_title = soup.find('h1').text
    except:
    # if game_title is None
        return 'NULL'
    return game_title


def __game_score(soup):
    """Returns the game score of of 5 (highest)"""
    try:
        game_score = soup.find(class_="rating productcard-rating__score").text
        game_score = float(re.search(r'(\d{1}\.?\d?)/', game_score).group().replace(r'/',''))
    except AttributeError:
        return 'NULL'
    return game_score


def __game_price_base(soup):
    """Returns the game prices"""
    try:
        game_price_base = float(soup.find("span", {"class": "product-actions-price__base-amount _price"}).text)
    except:
        # if game_price_base is None
        return "NULL"
    return game_price_base


def __game_price_final(soup):
    """Returns the game prices"""
    try:
        game_price_final = float(soup.find("span", {"class": "product-actions-price__final-amount _price"}).text)
    # if game_price_final is None:
    except:
        return "NULL"
    return game_price_final


def __game_price_discount(game_price_base, game_price_final):
    """Returns the discount of the game. If no discount returns zero"""
    no_discount = 0.00

    if game_price_base == game_price_final or game_price_base == 'NULL' or game_price_final == 'NULL':
        return no_discount
    else:
        return round((float(game_price_base) - float(game_price_final)) / float(game_price_base), 2)


def __check_game_page_url_response(game_page_url):
    """Verify game page url response"""
    if game_page_url.status_code != 200:
        return False
    else:
        return True


def game_data(game_page_url, soup):
    game_data_dict = {}  # The data of the game

    if not __check_game_page_url_response(game_page_url):
        raise ConnectionError(f"URL Response fail{game_page_url}")



    # game title
    game_data_dict['game_title'] = __game_title(soup)
    if game_data_dict['game_title'] == 'NULL':
        raise ValueError("No game title, not printing data")

    game_data_dict['game_sku'] = __game_sku(soup)
    game_data_dict['game_score'] = __game_score(soup)
    game_data_dict['game_price_base'] = __game_price_base(soup)
    game_data_dict['game_price_final'] = __game_price_final(soup)
    game_data_dict['game_price_discount'] = __game_price_discount(game_data_dict['game_price_base'], game_data_dict['game_price_final'])
    game_data_dict['game_url'] = game_page_url.url
    return game_data_dict