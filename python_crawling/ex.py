from bs4 import BeautifulSoup
import requests

url = "https://steemit.com/kr/@centering/1010"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
soup.prettify()
# print(soup)
table = soup.select_one('ol')
lis = table.find_all('li')

for li in lis:
    print(li.text)