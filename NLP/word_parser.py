# pip install konlpy # 한국어 parser
import os

from konlpy.tag import Okt
okt = Okt()
test = "안녕하세요 저는 펭수 입니다. 만나서 방가! ^^"

parser_data = okt.pos(test)
# nonus = okt.nouns(test) # 명사만 가져오기
# print(parser_data)

nonus = []
path = "./it/"
for file in os.listdir(path):
    with open(path + file, 'r', encoding="UTF-8") as f:
        text = f.read()
        nonus += okt.nouns(text)
words = [n for n in nonus if len(n) > 1]
print(words)
# pip install wordcloud
from collections import Counter
from wordcloud import WordCloud

cnt_word = Counter(words)
print(cnt_word)
wc = WordCloud(font_path='./NanumGothicBold.ttf', width=400, height=400
               , scale=2.0, max_font_size=250, background_color="white")
gen = wc.generate_from_frequencies(cnt_word)
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(gen)
wc.to_file("news.png")
plt.show()