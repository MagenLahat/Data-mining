"""
Project: Data-Mining GOG (Good Old Games)
Import URLs FIle
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
import config


def get_game_urls(gog_url):
    """
    Goes through the website pages and fetch all game urls
    :return: a list of all games urls
    """   
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox") 
    service_args = ['--verbose']    
    driver = webdriver.Chrome(os.path.join(os.getcwd(), config.CHROMEDRIVER_NAME), chrome_options=options, service_args=service_args)
    
    index = config.FIRST_PAGE_INDEX
    game_urls = []
    while index:

        # Ignore: for testing and QA.
        # if index == 3:
        #     break

        list_length = len(game_urls)
        driver.get(gog_url + str(index))
        if index > config.FIRST_PAGE_INDEX and driver.current_url == config.GOG_URL:  # if it returns to the first
            # page finish
            break

        try:
            elms = WebDriverWait(driver, config.TEN_SECONDS).until \
                (EC.presence_of_all_elements_located((By.TAG_NAME, config.MAIN_TAG)))
            for elem in elms:
                href = elem.get_attribute(config.HREF)
                if href is not None and href.startswith(config.GAMES_URL_PATH):
                    game_urls.append(href)
            print(f"Fetched games from page {index}")
            index += 1
        except EC.StaleElementReferenceException:
            print(f'stale element reference raised for page {index}, skipping page...')
            sleep(config.TEN_SECONDS)
            index += 1

        except ConnectionRefusedError:
            print(f'connection refused error raised {index}, skipping page...')
            sleep(config.TEN_SECONDS)
            index += 1
        list(set(game_urls))
        if len(game_urls) - list_length < 5:
            break
    driver.quit()
    return list(set(game_urls))
