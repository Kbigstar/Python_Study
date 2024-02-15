from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import time

driver = webdriver.Chrome()
url = "https://www.melon.com/chart/index.htm"
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup.prettify())

tbody = soup.find('tbody')
trs = tbody.find_all('tr')
arr = []
for tr in trs:
    # print(tr)
    tds = tr.find_all('td')
    # print(tds[1])
    # print(tds[5])

    ranks = tds[1].find_all('span')
    # print(ranks[0].text)
    # rank = tds[1].select_one('span.rank').text
    rank = ranks[0].text

    a_tags = tds[5].find_all('a')
    song = a_tags[0].text
    singer = a_tags[1].text

    print(rank,"위", song, " - ", singer)

    arr.append([rank, song, singer])
# print(arr)