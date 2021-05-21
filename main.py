"""
Project: Data-Mining GOG (Good Old Games)u
Students: Roy and Magen
Main File - Please run this file to start the script
"""

import arguments_parser
import grequests
import db_creator
import config
import time
from game_scrapper import game_page_scrapper
from import_urls import get_game_urls
from mysql_writer import WebsiteDB
from api_twitch import ApiTwitch
from SMS import sendSMS
from datetime import datetime


if __name__ == '__main__':
    print("""
            ***********************************
            Good Old Games Scrapper has Started
            ***********************************
            """)
    sms_resp = sendSMS(f"Started SCRAPPING GOG AT {datetime.now()}")
    print(sms_resp)

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
    counter = 0
    for game_page in get_game_urls(gog_url_partial):
        print(f"game counter {counter}")
        counter += 1
        url_batch.append(game_page)
        if len(url_batch) == config.BATCH_SIZE:
            print("Batch Size is Full, writing to DB")
            responses = (grequests.get(link) for link in url_batch)

            for response in grequests.map(responses):
                try:
                    game_data = game_page_scrapper(response)

                    if args.choice == 'screen' or args.choice == 'both':
                        print(game_data)

                    list_of_games_dict.append(game_data)
                except Exception as ex_message:
                    print("Issue 1")
                    print(ex_message)

            if args.choice == 'db' or args.choice == 'both':
                try:
                    with WebsiteDB(list_of_games_dict) as db:
                        print("hi")
                        db.write_game_titles()
                        db.write_game_genres()
                        db.write_game_prices()
                        db.write_game_scores()
                except Exception as ex_message:
                    print(ex_message)

            list_of_games_dict.clear()
            url_batch.clear()

    sms_resp = sendSMS(f"Finished SCRAPPING GOG AT {datetime.now()}")
    print(sms_resp)
