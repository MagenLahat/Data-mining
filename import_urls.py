"""
Project: Data-Mining GOG (Good Old Games)
Import URLs FIle
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import config


def get_game_urls(gog_url):
    """
    Goes through the website pages and fetch all game urls
    :return: a list of all games urls
    """
    driver = webdriver.Chrome(os.path.join(os.getcwd(), config.CHROMEDRIVER_NAME))
    index = config.first_page_index
    game_urls = []
    while index:
        # if index == 2:  # todo: to delete at the end.
        #     break

        driver.get(gog_url + str(index))
        if index > config.first_page_index and driver.current_url == config.gog_url:  # if it returns to the first
            # page finish
            break
        try:
            elms = WebDriverWait(driver, config.TEN_SECONDS).until\
                (EC.presence_of_all_elements_located((By.TAG_NAME, config.main_tag)))
            for elem in elms:
                href = elem.get_attribute(config.href)
                if href is not None and href.startswith(config.games_url_path):
                    game_urls.append(href)
            index += 1
        except EC.StaleElementReferenceException:
            print(f'stale element reference raised for page {index}, skipping page...')
            sleep(config.TEN_SECONDS)
            index += 1

        except ConnectionRefusedError:
            print(f'connection refused error raised {index}, skipping page...')
            sleep(config.TEN_SECONDS)
            index += 1
    driver.quit()
    return list(set(game_urls))
