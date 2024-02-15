import csv
import requests
from bs4 import BeautifulSoup
# csv파일 읽기
with open('musinsa.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='|')
    data = list(reader)
    for row in data:
        url = "https://www.musinsa.com" + row[1]
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        content = soup.select_one('#vContent .viewContents').text
        print(content)

