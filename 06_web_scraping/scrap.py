from selenium import webdriver
import pandas as pd
import platform
from time import sleep


def get_daum_news_data_dict(url, num_scroll=0):
    """Get news data from the given URL."""

    # define data dict
    data_dict = {
        'title': [],
        'text': [],
        'url': [],
        'publisher': [],
        'dt': []
    }

    # get the driver_path
    print(platform.system())
    if platform.system() == 'Windows': # windows
        driver_path = './chromedriver.exe'
    elif platform.system() == 'Darwin': # mac
        driver_path = './chromedriver'

    # create a webdriver instance
    cService = webdriver.ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service = cService)
    driver.implicitly_wait(3) # waiting 3 seconds

    # access the url
    driver.get(url)
    driver.implicitly_wait(2) # wait 2 seconds for loading the webpage

    # scroll down
    for _ in range(num_scroll):
        driver.find_element('css selector', 'a.link_moreview').click()
        sleep(5) # wait 5 seconds for loading the webpage

    # find all news elements
    news_elements = driver.find_elements('css selector', '#newsData > ul > li')

    # scrap data
    for news in news_elements:
        title_el = news.find_element('css selector', 'a.link_txt')
        text_el = news.find_element('css selector', 'a.link_desc')
        # dt_el, publisher_el = news.find_elements('css selector', 'span.txt_info')
        dt_el = news.find_element('css selector', 'span.txt_info')
        publisher_el = news.find_element('css selector', 'span.txt_info:nth-child(2)')
        
        url = title_el.get_attribute('href')
        title = title_el.text
        text = text_el.text
        dt = dt_el.text
        publisher = publisher_el.text

        data_dict['title'].append(title)
        data_dict['text'].append(text)
        data_dict['dt'].append(dt)
        data_dict['url'].append(url)
        data_dict['publisher'].append(publisher)

    return data_dict


if __name__ == '__main__':
    url = 'https://sports.daum.net/worldsoccer/news/breaking'
    data_dict = get_daum_news_data_dict(url, num_scroll=3)
    df = pd.DataFrame(data_dict)
    df.to_csv('soccer_news.csv', index=False)