# import requests
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

game_urls = []
PATH = '/home/magen/chromedriver'
driver = webdriver.Chrome(PATH)
index = 1

while index:

    driver.get("https://www.gog.com/games?sort=popularity&page=" + str(index))
    if index > 1 and driver.current_url == "https://www.gog.com/games?sort=popularity&page=1": # if it returns to the first page finish
        break
    try:
        element = WebDriverWait(driver, 10).until(    # wait until the element is loaded
            EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
       # common selenium exception for items that were not loaded on time
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None and href.startswith("https://www.gog.com/game/"):
                game_urls.append(href)
        index += 1
    except StaleElementReferenceException:
        print(f'stale element reference raised for page {index}, retrying')
        driver.quit()
        sleep(10)

driver.quit()
game_urls = list(set(game_urls))
for url in game_urls:
    print(url)


