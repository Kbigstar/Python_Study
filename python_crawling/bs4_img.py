from bs4 import BeautifulSoup
import requests
import urllib.request as req
import os

image_path ="./img"
# 폴더가 없으면 생성
if not os.path.exists(image_path):
    os.mkdir(image_path)

url ="https://search.daum.net/search?w=tot&DA=TMZ&q=일간영화순위"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
ol = soup.select_one('.type_plural.list_exact.movie_list')
lis = ol.find_all('li')
for li in lis:
    if None is li.get('class'):
        title = li.select_one('.wrap_cont .info_tit').text.replace(':','')
        img = li.find('img')['data-original-src']
        if img:
            req.urlretrieve(img, os.path.join(image_path, title.strip()+'.png'))
# 이미지 저장 urlretrieve('저장할 이미지의 url', '로컬에 저장할이름')
# img_url='https://search1.kakaocdn.net/thumb/R232x328.fwebp.q85/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fmovie%2F64f1b6569bc26bde31a7f1d223895ca76078394c'
# req.urlretrieve(img_url, 'test.png')


