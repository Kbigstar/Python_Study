html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2" /> and
<a href="http://example.com/tillie" class="sister">Tillie</a>
<a href="http://example.com/tillie" class="sister">한글</a>
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
# 구조화되게 출력
# print(soup.prettify())
a_tag = soup.a
print(a_tag.name)
print(a_tag.text)
print(a_tag['href'])   #속성 명으로 접근
print(a_tag.get('id')) # get 함수(속성명으로 찾음)
# find 1개의 태그(첫번째 등장하는)
# find_all : 동일 태그 모두
a_all = soup.find_all('a')
# print(a_all)
for a in a_all:
    print(a.text)
a_all2 = soup.find_all('a', string=True) #text가 있는 a태그만
print(len(a_all2))
import re
# re 정규표현식 관련 라이브러리

a_l = soup.find_all('a', string=re.compile('l')) # l 이 존재하는
a_han = soup.find('a', string=re.compile('[가-힝]'))  #한글이 존재하는
print('l포함', a_l)
print('한글포함', a_han)

# select :다건 css 셀렉터사용
# select_one : 한건
link1 = soup.select_one('#link1')
cls = soup.select('.sister')
print(link1)
print(cls)

