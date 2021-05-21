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
from mysql_writer import WebsiteDB
import db_creator
from api_twitch import ApiTwitch

proxies = {'http': 'http://10.10.1.10:3128',
           'https': 'http://10.10.1.10:1080'}

if __name__ == '__main__':
    list_of_games_dict = []  # list of all batches into mysql_data_mining
    gog_url_partial, args = arguments_parser.filter_args()

    # Twitch API
    """The new API Inegration"""

    if args.twitch == "yes":
        api = ApiTwitch()
        call = api.api_twitch_to_mysql()

    if args.db == 'yes': # creates the database schema if -d was chosen yes
        db_creator.create_db()

    url_batch = []  # list of urls for grequests
    for game_page in get_game_urls(gog_url_partial):
        url_batch.append(game_page)
        if len(url_batch) == config.BATCH_SIZE:
            responses = (grequests.get(link, proxies=proxies) for link in url_batch)

            for response in grequests.map(responses):
                try:
                    game_data = game_page_scrapper(response)

                    if args.choice == 'screen' or args.choice == 'both':
                        print(game_data)

                    list_of_games_dict.append(game_data)
                except Exception as ex_message:
                    print(ex_message)

            if args.choice == 'db' or args.choice == 'both':
                try:
                    with WebsiteDB(list_of_games_dict) as db:
                        db.write_game_titles()
                        db.write_game_genres()
                        db.write_game_prices()
                        db.write_game_scores()
                except Exception as ex_message:
                    print(ex_message)
            list_of_games_dict.clear()
            url_batch.clear()
