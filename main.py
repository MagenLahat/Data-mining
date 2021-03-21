"""
Project: Data-Mining GOG (Good Old Games)u
Students: Roy and Magen
Main File - Please run this file to start the script
"""
# todo: update requirements before hand-in.
# todo: update CONST
# todo: fix function names
# todo: functions type hint
# todo: update md5 documentation - cli + mysql (creation of db and inserts)
# todo: md5 using typora / smooth markdown
import arguments_parser
import grequests
import config
from game_scrapper import game_page_scrapper
from import_urls import get_game_urls
from mysql_writer import WebsiteDB

if __name__ == '__main__':

    list_of_games_dict = []
    gog_url_partial, args = arguments_parser.filter_args()

    url_batch = []  # list of urls for grequests
    for game_page in get_game_urls(gog_url_partial):
        url_batch.append(game_page)
        if len(url_batch) == config.BATCH_SIZE:
            responses = (grequests.get(link) for link in url_batch)

            for response in grequests.map(responses):
                try:
                    game_data = game_page_scrapper(response)

                    if args.choice == 'screen' or args.choice == 'both':
                        print(game_data)

                    list_of_games_dict.append(game_data)  # todo: for sql purpose
                except Exception as ex_message:
                    print(ex_message)

                    # list_of_games_dict = [{'game_title': 'Fallout 3: Game of the Year Edition', 'game_sku': 1248282609, 'game_score': 3.9, 'game_price_base': 19.99, 'game_price_final': 19.99, 'game_price_discount': 0.0, 'game_url': 'https://www.gog.com/game/fallout_3_game_of_the_year_edition', 'genre': ['Role-playing', 'FPP', 'Open World'], 'works_on': 'windows (7, 8, 10)', 'release_date': '2010-10-10', 'company': ['bethesda game studios', 'bethesda softworks llc'], 'size': None},
                    #                 {'game_title': 'Grim Dawn', 'game_sku': 1449651388, 'game_score': 4.5, 'game_price_base': 24.99, 'game_price_final': 6.24, 'game_price_discount': 0.75, 'game_url': 'https://www.gog.com/game/grim_dawn', 'genre': ['Action', 'Role-playing', 'Fantasy'], 'works_on': 'windows (7, 8, 10)', 'release_date': '2010-10-10', 'company': ['crate entertainment', 'crate entertainment'], 'size': 3600.0}]

                    # todo: writing to sql
                    if args.choice == 'db' or args.choice == 'both':
                        try:
                            with WebsiteDB(list_of_games_dict) as db:
                                db.write_game_titles()
                                db.write_game_genres()
                                db.write_game_prices()
                                db.write_game_scores()
                        except Exception as ex_message:
                            print(ex_message)

            url_batch.clear()





