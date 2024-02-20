import requests
from bs4 import BeautifulSoup
import sqlite3

def get_price(code):
    url = "https://finance.naver.com/item/main.naver?code="+code
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    today = soup.find('div', {'class':'today'})
    price = today.find('em').find('span', {'class': 'blind'}).text
    price = price.replace(',', '')
    return price
if __name__ == '__main__':
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock WHERE market='KOSPI' AND use_yn ='Y' ")
    rows = cur.fetchall()  # 전체   한개 fetchone(), 몇몇fetchmany(3)
    conn.close()
    for row in rows:
        print(get_price(row[0]), row[1])

