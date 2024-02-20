from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
url = "https://www.hanatour.com/package/international"
search_word =""
# 백그라운드 실행되도록 (크롬드라이버)
option = webdriver.ChromeOptions()
option.add_argument('--headless')
def fn_search():
    global search_word
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=option) # 백 그라운드 실행 옵션추가
    driver.get(url)
    time.sleep(1)
    search_word = entry.get() # 입력값
    input_search = driver.find_element(By.ID, 'input_keyword')
    input_search.send_keys(search_word)
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
            txt.insert(END, title+'\n')
        except Exception as e:
            print(str(e))
from tkinter import *
app = Tk()
app.title("tour search")
entry = Entry(app, width=100)
entry.pack()
btn = Button(app, text='search', command=fn_search)
btn.pack()
txt = Text(app, width=100, height=50)
txt.pack()
app.mainloop()
