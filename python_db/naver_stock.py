import requests
from bs4 import BeautifulSoup
url = "https://finance.naver.com/item/main.naver?code=005930"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
today = soup.find('div', {'class':'today'})
price = today.find('em').find('span', {'class': 'blind'}).text
print(price)
# print(soup.prettify())