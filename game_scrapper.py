# TODO: HEADLINE
""""""
from import_game_details import game_details
from import_game_data import game_data
import config


from bs4 import BeautifulSoup

def game_page_scrapper(game_page_url):
    """
    Returns ALL the available data from the game's page url.
    :param game_page_url: Response object (requests library)
    :return: game_sql(dict) with all the game info.
    """
    soup = BeautifulSoup(game_page_url.content, features="lxml")
    # Game data section
    game_data_dict = game_data(game_page_url, soup)

    # Game details section
    game_details_dict = game_details(soup)

    # Merging general data with game details section
    game_sql = {**game_data_dict, **game_details_dict}
    return game_sql
