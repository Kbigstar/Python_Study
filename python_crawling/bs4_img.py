from bs4 import BeautifulSoup
import requests
import urllib.request as req

url = "https://search.daum.net/search?w=tot&DA=TMZ&q=일간영화순위"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
ol = soup.select_one('.type_plural.list_exact.movie_list')
lis = ol.find_all('li')
for li in lis:
    if None is li.get('class'):
        title = li.select_one('.wrap_cont .info_tit').text
        img = li.find('img')['data-original-src']
        req.urlretrieve(img, title.strip()+'.png')
# 이미지 저장 urlretrieve('저장할 이미지의 url', '로컬에 저장할 이름')
# img_url = 'https://search1.kakaocdn.net/thumb/R232x328.fwebp.q85/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fmovie%2F630a0a90f481f8dc6692d63131b6fc6076c6d0e2'
# req.urlretrieve(img_url,'test2.png')