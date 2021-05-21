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
GOG_URL = "https://www.gog.com/games?sort=popularity&page=1"
ROOT_TAG = 'https://www.gog.com/games?sort=rating'
PRICE_TAG = '&price='
TAB_TAG = '&tab='
PAGE_TAG = '&page='

# IMPORT_URLS CONSTANTS
CHROMEDRIVER_NAME = 'chromedriver'
BATCH_SIZE = 10
TEN_SECONDS = 10
MAIN_TAG = "a"
HREF = 'HREF'
GAMES_URL_PATH = "https://www.gog.com/game/"
FIRST_PAGE_INDEX = 1

#GAME SCRAPPER CONSTANTS
BEAUTIFUL_SOUP_FEATURE = 'lxml'

# GAME DATA CONSTANTS
GAME_SKU_FIND_CLASS = "layout"
GAME_SKU_FIND_ATTR = "card-product"
GAME_TITLE_FIND_TAG = 'h1'
GAME_SCORE_FIND_CLASS = "rating productcard-rating__score"
GAME_SCORE_SEARCH_REGEX = r'(\d{1}\.?\d?)/'
GAME_SCORE_REGEX_SLASH = r'/'
SPAN_TAG = "span"
CLASS_TAG = "class"
DIV_TAG = "div"
GAME_PRICE_BASE_TEXT = "product-actions-price__base-amount _price"
GAME_PRICE_FINAL_TEXT = "product-actions-price__final-amount _price"
URL_GOOD_RESPONSE = 200

KEYNAME_GAME_TITLE = "game_title"
KEYNAME_GAME_SKU = "game_sku"
KEYNAME_GAME_SCORE = "game_score"
KEYNAME_GAME_BASE_PRICE = "game_price_base"
KEYNAME_GMAE_FINAL_PRICE = "game_price_final"
KEYNAME_GAME_DISCOUNT = "game_price_discount"
KEYNAME_GAME_URL = "game_url"
NO_GAME_TITLE_ERROR_MESSAGE = "No game title, not printing data"

# GAME DETAILS CONSTANTS
PUNCTUATION_MARK = r'[:]'
WORD_REGEX = r'\w+ \w+'
KEYNAME_GENRE = 'genre'
KEYNAME_WORKS_ON = 'works_on'
KEYNAME_RELEASE_DATE = 'release_date'
KEYNAME_COMPANY = 'company'
KEYNAME_GAME_SIZE = 'size'
GAME_KEYS = [KEYNAME_GENRE, KEYNAME_WORKS_ON, KEYNAME_RELEASE_DATE, KEYNAME_COMPANY, KEYNAME_GAME_SIZE]
DATETIME_REGEX = r'\d{4}-\d{2}-\d{2}'
TO_MB_SCALE = 1000
GAME_IN_GB_SIZE = "gb"
GAME_IN_KB_SIZE = "kb"
game_details_text = "details__content table__row-content"
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# mysql_data_mining Connection Constants
MYSQL_DATABASE = "GOG_SCRAPPER_DB"
MYSQL_HOST = "localhost"
MYSQL_AUTH = 'mysql_native_password'
# mysql_data_mining Connection Variables
mysql_user = "root"
mysql_password = "Itc12345!"
mysql_native_authentication = False

# Twitch API
API_CLIENT_ID = "honcjjterpsdgqkmbja3a1688oqnvp"
API_CLIENT_SECRET = "8qmn61l90ny1k1nb2ujwtl9qujgvlt"
