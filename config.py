"""
Project: Data-Mining GOG (Good Old Games)
Config File - Contains all the CONSTANTS AND SETUPS for the whole project
"""
# General
NULL_VALUE = None
EMPTY_STRING = ""
SPACE_STRING = " "
UNDERLINE = "_"
NEW_LINE = r'[\n]'
LINE_SPACED = " - "
SLASH_STRING = r'/'
gog_url = "https://www.gog.com/games?sort=popularity&page=1"
gog_url_partial = "https://www.gog.com/games?sort=popularity&page="

# IMPORT_URLS CONSTANTS
CHROMEDRIVER_NAME = 'chromedriver'
BATCH_SIZE = 10
TEN_SECONDS = 10
main_tag = "a"
href = 'href'
games_url_path = "https://www.gog.com/game/"
first_page_index = 1

#GAME SCRAPPER CONSTANTS
BEAUTIFUL_SOUP_FEATURE = 'lxml'

# GAME DATA CONSTANTS
game_sku_find_class = "layout"
game_sku_find_attr = "card-product"
game_title_find_tag = 'h1'
game_score_find_class = "rating productcard-rating__score"
game_score_search_regex = r'(\d{1}\.?\d?)/'
game_score_regex_slash = r'/'
SPAN_TAG = "span"
CLASS_TAG = "class"
DIV_TAG = "div"
game_price_base_text = "product-actions-price__base-amount _price"
game_price_final_text = "product-actions-price__final-amount _price"
URL_GOOD_RESPONSE = 200

keyname_game_title = "game_title"
keyname_game_sku = "game_sku"
keyname_game_score = "game_score"
keyname_game_base_price = "game_price_base"
keyname_gmae_final_price = "game_price_final"
keyname_game_discount = "game_price_discount"
keyname_game_url = "game_url"
no_game_title_error_message = "No game title, not printing data"

# GAME DETAILS CONSTANTS
PUNCTUATION_MARK = r'[:]'
WORD_REGEX = r'\w+ \w+'
keyname_genre = 'genre'
keyname_works_on = 'works_on'
keyname_release_date = 'release_date'
keyname_company = 'company'
keyname_game_size = 'size'
game_keys = [keyname_genre, keyname_works_on, keyname_release_date, keyname_company, keyname_game_size]
DATETIME_REGEX = r'\d{4}-\d{2}-\d{2}'
TO_MB_SCALE = 1000
GAME_IN_GB_SIZE = "gb"
GAME_IN_KB_SIZE = "kb"
game_details_text = "details__content table__row-content"
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# MySQL Connection
MYSQL_DATABASE = "gog_scrapper_db"
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "itc12345" # todo: delete password of mysql