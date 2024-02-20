from bs4 import BeautifulSoup
from selenium import webdriver
import time
driver = webdriver.Chrome()
url = 'https://www.melon.com/chart/index.htm'
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
tbody = soup.find('tbody')
trs = tbody.find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    rank = tds[1].select_one('span.rank').text
    a_tag = tds[5].find_all('a')
    title = a_tag[0].text
    singer = a_tag[1].text
    print(rank, title, singer)


