# pip install selenium
# pip install chromedriver_autoinstaller
from selenium import webdriver
import chromedriver_autoinstaller
import time
# selenium은 브라우저를 컨트롤 해야하기 때문에 브라우저 드라이버 설치
chromedriver_autoinstaller.install()
# 브라우저 오픈
driver = webdriver.Chrome()
driver.implicitly_wait(3) # 브라우저가 켜질때까지 기다리기
url ="https://www.msn.com/ko-kr/news/techandscience"
driver.get(url) # url 페이지로 이동
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
pagedown = 1
cnt = 10
body = driver.find_element(By.TAG_NAME, 'body') # 엘리먼트 찾는 함수
while pagedown < cnt:
    body.send_keys(Keys.PAGE_DOWN) # 스크롤 내리기
    time.sleep(1)
    pagedown += 1
soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup.prettify())
driver.quit()