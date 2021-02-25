# TODO: HEADLINE
""""""
import grequests
import config

# todo:new files
from game_scrapper import game_page_scrapper
from import_urls import get_game_urls


if __name__ == '__main__':
    urls_to_send = []  # list of urls for grequests
    # TODO: get_game_urls
    for game_page in get_game_urls():
        # TODO: Change urls_to_send name
        urls_to_send.append(game_page)
        if len(urls_to_send) == config.BATCH_SIZE:
            # TODO: CHANGE grs name
            grs = (grequests.get(link) for link in urls_to_send)

            for request in grequests.map(grs):
                try:
                    # rs = requests.get(request)
                    game_data = game_page_scrapper(request)
                    print(game_data)

                except Exception as ex_message:
                    print(ex_message)
            urls_to_send.clear()





