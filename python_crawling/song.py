from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
song = input("노래제목 : ")
singer = input("가수이름 : ")
msg = "가사"
q = singer+" "+song+" "+msg
oq = song + " " + msg
url =f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query={quote_plus(q)}&oquery={quote_plus(oq)}&tqi=iN34zwqo1fsssTDlNKRssssssAo-100978'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

lyrics = soup.select_one('.intro_box')
for ly in lyrics:
    print(ly.text)
