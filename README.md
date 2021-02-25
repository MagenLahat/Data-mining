# DATA MINING PROJECT
Data mining project - Roy and Magen
#DESCRIPTION
In this project so far, we chose to scrape the website GOG.com (https://www.gog.com/).
GOG.com is a digital distribution platform – an online store with a curated selection of games,
an optional gaming client giving you freedom of choice, 
and a vivid community of gamers.
Each game on the page was scraped for the data given on the page.
Details scraped from each game: game_title, game_sku, game_score, game_price_base, game_price_final, 
game_price_discount, game_url, genre, works_on (supported operating systems), release_date, company.
#INSTALLATION AND SUPPORT
The code is using at the moment selenium webdriver for google chrome driver.
Google chrome must be installed, and the driver's path needs to be copied to the config file.
For downloading the chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
The chromedriver version must be compatible with the google chrome version 
#INSTRUCTIONS
To execute the program, main.py should be executed. The chrome browser will pop out until all the pages will be
collected. Each game details will be printed in one line to std output.  
#PROJECT FILES MODULES
main.py - calls the import urls module, gets all the game urls and uses grequest to get the responses concurrently 
in batches. Each response is sent to game_page_scrapper.py which returns the details in text, and is printed there.

import_urls.py - goes through the website pages and parses all game urls, returns a list of all games urls.

game_scrapper.py - Returns ALL the available data from the game's page url. parameters: game_page_url,
Response object (requests library). returns game_sql(dict) with all the game info.

import_game_details.py - Contains all the functions that scrape the data, uses bs4.

import_game_data.py - Merging general data with game details

config.py - contains constants, key strings and urls.

#GIT HUB REPOSITORY
https://github.com/MagenLahat/Data-mining.git

#CONTACT SUPPORT
magat261@gmail.com

roy.toled@gmail.com


