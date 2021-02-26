# DATA MINING PROJECT
Data mining project - Roy and Magen
#DESCRIPTION
In this project so far, we chose to scrape the website GOG.com (https://www.gog.com/).
GOG.com is a digital distribution platform – an online store with a curated selection of games,
an optional gaming client giving you freedom of choice, 
and a vivid community of gamers.

GOG scrapping for the given data:

game_title - The game title,

game_sku - The game stock keeping unit,

game_score - The score of the game, given by the gamers,

game_price_base - The base price in (USD),

game_price_final - The final price after discount (USD), 

game_price_discount - The percentage of discount,

game_url - The URL of the specific game,

genre - List of game's genre,

works_on (supported operating systems) - i.e. macOS/Windows/Linux etc...,

release_date - The game release data,

company - List of development & publishers of the game.
#INSTALLATION AND SUPPORT
To Scrap the site, we had to use several external libraries, such as bs4 and Selenium. 
You can find all the required libraries in the added requirements.txt file.
To run the script on your local machine, please install those libraries.

After installing these libraries, we suggest focusing on "selenium webdriver". 

Selenium can work with different browsers. We decided to go on with the most popular today, Google Chrome. 
Therefore:
1. Please verify that google chrome is installed on your local machine.
2. On google chrome itself, click the 3 dots on the URL bar -> Help -> About google chrome -> Copy your google chrome version
 (for example: Version 88.0.4324.190 (Official Build) (64-bit)).
3. Enter the following link: https://sites.google.com/a/chromium.org/chromedriver/downloads
4. Find your chrome version from step 2, choose your current operating system (macOS, Linux, etc...)
 and download the zip file to your local machine.
5. The zip file contains a file called 

* chromedriver, which needs to be added to the folder of the main script.

* chromedriver responsible for the automation and communication between the python script and the browser itself. 
Attention: In some cases, it requires downloading few versions until you find the correct one. 
By default, we left chromedriver.exe, which compatible with Win 64 & Chrome 88.0.4324.190. Make sure you replace it with your chromedriver.
 
#INSTRUCTIONS
In order to start the scrapping work, please run the main.py file using Python. The chrome browser will pop out until
all the pages will be collected. Please don't touch the computer at that time, since it can hurt the process
of Selenium. There are over 98 pages in GOG. Therefore it can take some time.
So you're asking why it's taking so long?
Basically, on each page, we collect all the game URLs. 
Usually, the chrome opens over the script, so you can't see what is printed (And please don't try, 
it can hurt Selenium).
From time to time, we print which pages aren't scrapped.

After we finished collecting all games' URLs, you'll start to see how the script is printing to
 stdout each game's detail in a row. 

#PROJECT FILES MODULES
main.py - calls the import URLs module, gets all the game URLs, and uses grequest to get the responses concurrently
 in batches. Each response is sent to game_page_scrapper.py, which prints the game data into stdout. 

import_urls.py - goes through the website pages and parses all game URLs, returns a list of all games URLs.

game_scrapper.py - Returns ALL the available data from the game's page URL. parameters: game_page_url,
Response object (requests library). Returns game_sql with all the game info.

import_game_details.py - Contains all the functions that scrape the data, uses bs4.

import_game_data.py - Merging general data with game details

config.py - contains constants, key strings, and URLs.

#GIT HUB REPOSITORY
https://github.com/MagenLahat/Data-mining.git

#CONTACT FOR SUPPORT
magat261@gmail.com

roy.toled@gmail.com


