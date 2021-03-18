"""
Project: Data-Mining GOG (Good Old Games)u
Students: Roy and Magen
Main File - Please run this file to start the script
"""
import arguments_parser
import grequests
import config
from game_scrapper import game_page_scrapper
from import_urls import get_game_urls


if __name__ == '__main__':

    gog_url_partial = arguments_parser.filter_args()

    url_batch = []  # list of urls for grequests
    for game_page in get_game_urls(gog_url_partial):
        url_batch.append(game_page)
        if len(url_batch) == config.BATCH_SIZE:
            responses = (grequests.get(link) for link in url_batch)

            for response in grequests.map(responses):
                try:
                    game_data = game_page_scrapper(response)
                    print(game_data)

                except Exception as ex_message:
                    print(ex_message)
            url_batch.clear()





