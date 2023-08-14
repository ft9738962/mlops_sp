from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils.config import get_config
from src.utils.directory_utils import find_root

class IMDB_SCRAPER:
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
        load_delay: int=1,
        ) -> None:
        '''
        Purpose: 抓数据
        Args
            url: str: 网址
            load_dealy: 延迟时间,默认1s
        Return: list(str): 数据
        '''
        # 初始化headless浏览器
        driver = self.web_driver_chrome()
        self.url=url
        driver.get(url)
        time.sleep(load_delay)
        
        corpus=[]
        start_index = 0

        while True:
            try:
                # 抓取需要的信息
                cards=driver.find_elements(By.XPATH,'//*[@id="main"]/section/div[2]/div[2]/div')
                cards = cards[start_index:]
                for card in cards:
                    corpus.append(card.text)
                
                # 找加载按钮并点击加载
                load_more_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="load-more-trigger"]'))
                )
                load_more_element.click()
                time.sleep(load_delay)

                # 计算加载后的位置
                start_index = len(corpus)
                print(start_index)
            except:
                break
        driver.quit()
        self.data = corpus
        print(f'get {len(corpus)} lines of comment')

    def save_date(self,
        file: Path | str,
        sep: str='<>?',
        allow_duplicated: bool=False,
        ):
        if not allow_duplicated:
            data = list(set(self.data))
        with open(file, 'w') as f:
            f.write(sep.join(data))
            print(f'write {len(data)} (raw: {len(self.data)}) lines of comment')

if __name__ == "__main__":
    url="https://www.imdb.com/title/tt15398776/reviews?spoiler=hide&sort=submissionDate&dir=desc&ratingFilter=0"
    imdb_scraper=IMDB_SCRAPER()
    imdb_scraper.get_data(url, 3)
    imdb_scraper.save_date(
        find_root() / 
        get_config()['filepath']['raw_txt']
        )

