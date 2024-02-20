from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
url = "https://www.hanatour.com/package/international"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(1)
input_search = driver.find_element(By.ID, 'input_keyword')
input_search.send_keys('하와이')
driver.find_element(By.CSS_SELECTOR,'button.btn_search').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="contents"]/div[3]/div[1]/div[1]/a').click()
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
arr = soup.select('.prod_list li')
for li in arr:
    try:
        title = li.select_one('.txt_info .tit').text
        print(title)
    except Exception as e:
        print(str(e))


