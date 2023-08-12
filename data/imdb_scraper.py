from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class imdb:

    def web_driver_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)
    
    def get_data(self,
        url: str, 
        load_delay: int=2):
        try:
            driver = self.web_driver_chrome()
            self.url=url

            driver.get(url)

            time.sleep(load_delay)
            corpus=[]
            start_index = 0

            while True:
                try:
                    cards=driver.find_elements(By.XPATH,'//*[@id="main"]/section/div[2]/div[2]/div')
                    cards = cards[start_index:]
                    
                    for card in cards:
                        corpus.append(card.text)
                        
                    load_more_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="load-more-trigger"]'))
                    )
                    load_more_element.click()
                    time.sleep(load_delay)
                    start_index = len(corpus)
                    print(start_index)
                except:
                    break
            driver.quit()
            return corpus  
        except:
            logging.error("Invalid url")

if __name__ == "__main__":
    url="https://www.imdb.com/title/tt15398776/reviews/?spoiler=hide"
    imdb_scraper=imdb()
    corpus=imdb_scraper.get_data(url, 3)
    corpus = list(set(corpus))
    with open('corpus.txt', 'w') as f:
        f.write('<>?'.join(corpus))
