# TODO: HEADLINE
""""""
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import os
import config


def get_game_urls():
    """
    goes through the website pages and parses all game urls
    :return: a list of all games url
    """

    driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
    index = 1
    game_urls = []
    while index:
        # todo: remove after finish
        if index == 5:
            break

        driver.get(config.gog_url_partial + str(index))
        if index > 1 and driver.current_url == config.gog_url:  # if it returns to the first page finish
            break
        try:
            element = WebDriverWait(driver, 10).until(  # wait until the element is loaded
                EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            # common selenium exception for items that were not loaded on time
            elems = driver.find_elements_by_tag_name('a')
            # sleep(10)
            for elem in elems:
                href = elem.get_attribute('href')
                if href is not None and href.startswith("https://www.gog.com/game/"):
                    # print(href) #todo: delete after we finish
                    game_urls.append(href)
            index += 1
        except EC.StaleElementReferenceException:
            print(f'stale element reference raised for page {index}, skipping page...')
            sleep(10)
            index += 1

        except ConnectionRefusedError:
            print(f'connection refused error raised {index}, skipping page...')
            sleep(10)
            index += 1
    driver.quit()
    return list(set(game_urls))