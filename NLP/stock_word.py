from DBManager import DBManager
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
mydb = DBManager()

# 005930 삼성 전자
param = input("워드 클라우드를 보고싶은 종목코드를 입력! : ")
sql = """SELECT * FROM stock_bbs WHERE code=:1"""
df = pd.read_sql(con=mydb.conn, sql=sql, params=[param])
nouns = []
okt = Okt()
for idx, row in df.iterrows():
    if row['CONTENTS']:
        nouns += okt.nouns(row['CONTENTS'])
words = [n for n in nouns if len(n) > 1] # 두글자 단어부터
count = Counter(words)
print(count)

wc = WordCloud(font_path='./NanumGothicBold.ttf', width=400, height=400
               , scale=2.0, max_font_size=250, background_color="white")
gen = wc.generate_from_frequencies(count)
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(gen)
wc.to_file("news.png")
plt.show()