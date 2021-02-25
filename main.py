# TODO: HEADLINE
"""Data mining project - Roy and Magen
"""


import grequests
import config

# todo:new files
from game_scrapper import game_page_scrapper
from import_urls import get_game_urls


if __name__ == '__main__':
    url_batch = []  # list of urls for grequests
    for game_page in get_game_urls(config.gog_url_partial):
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





