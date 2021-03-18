import argparse
import config


def filter_args():
    parser = argparse.ArgumentParser(description='search filters')
    parser.add_argument('-m', '--main_filter', help='main_filter',
                        choices=['everything', 'new', 'on_sale'], default='everything')
    parser.add_argument('-p', '--price_filter', help='price filter under 5,10,25 dollars, 25+ dollars, free or '
                                                     'discounted',
                        choices=['u5', 'u10', 'u15', 'u25', 'a25', 'free',
                                 'discounted'], default='')
    parser.add_argument('-c', '--choice', help='screen - print to screen, db - write to database or both',
                        choices=['screen', 'db', 'both'], default= 'screen')
    args = parser.parse_args()

    print(args)
    st = config.ROOT_TAG + config.PRICE_TAG + args.price_filter + config.TAB_TAG + args.main_filter + config.PAGE_TAG
    return st
