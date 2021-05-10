"""
Project: Data-Mining GOG (Good Old Games)
argument_parser - parses arguments from CLI select the program operation
arguments:
          -m: selects whether to scrape through  'everything' - every game for sale in the website (default)
                                                 'on_sale' - games that are on a temporary discount
                                                 'new' - games tht were recently released

          -p: price filter: 'u5', 'u10', 'u15' corresponds to games sold with prices under 5,10,15 usd
                            'a25' - games sold with price above 25 usd
                            'free' - games that are free to download
                            default - no price filter

          -c: users choice: 'screen' - print the results to the screen (default)
                            'db' - write the results to the Data-Bae
                            'both' - print the results to the screen and write them to the Data-Bae

CLI examples: <python3 main.py -m new -p u10 -c both> -> new games under 10 usd, prints both to screen and writes to
             the Data-Base

              <python3 main.py -c both>  ->scrapes through all games with no price filter, prints results to the screen
              and writes to db

              <python3 main.py -p free> -> scrapes through all the free games and writes them to the screen
"""

import argparse
import config
from argparse import RawTextHelpFormatter


def filter_args():
    # parser = argparse.ArgumentParser(description='search filters')
    parser = argparse.ArgumentParser(description='search filters', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-m', '--main_filter', help='''
                main_filter - will select the main page where the scraper will start to scrape from,
                three options:
                1. everything - every game for sale in the website (default)
                2. on_sale - games that are on a temporary discount 
                3. new - games that were recently released''',
                        choices=['everything', 'new', 'on_sale'], default='everything')
    parser.add_argument('-p', '--price_filter', help='''
                price filter - will filter prices: 
                u5 - under 5 usd
                u10 - under 10 usd
                u15 - under 15 usd
                u25 - under 25 usd
                a25 - above 25 usd
                free - free games
                discounted - games that are on sale with a discount
                ''',
                        choices=['u5', 'u10', 'u15', 'u25', 'a25', 'free',
                                 'discounted'], default='')
    parser.add_argument('-c', '--choice', help='''
                screen - print to screen 
                db - write to database
                both - print to screen and write to the database''',
                        choices=['screen', 'db', 'both'], default='screen')
    parser.add_argument('-d', '--db', help='''
                    yes - create the database schema and tables 
                    no - don't create it, if you know it exists or from some other reason (default)
                    ''',
                        choices=['yes', 'no'], default='no')

    args = parser.parse_args()


    full_link = config.ROOT_TAG + config.PRICE_TAG + args.price_filter + \
                config.TAB_TAG + args.main_filter + config.PAGE_TAG

    return full_link, args
