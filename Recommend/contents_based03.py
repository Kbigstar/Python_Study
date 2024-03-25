from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

reviews = ["이 제품 정말 좋아요. 다음에도 구매의향 있습니다"
           , "배송이 너무 늦어서 별로 였습니다."
           , "가격 대비 품질이 훌륭합니다."
           , "설명대로 제품이 도착해서 만족."
           , "제품이 고장나서 AS 받음"
           , "AS가 어려움"
           , "추천하고 싶은 제품입니다."]

okt = Okt()

def fn_token(doc):
    tokens = []
    pos_text = okt.pos(doc)
    for t in pos_text:
        token = "/".join(t)
        tokens.append(token)
    return tokens
print(fn_token(reviews[0]))

model = TfidfVectorizer(tokenizer=fn_token,
                        stop_words=["./Punctuation", "이/Noun", "가/Josa", "을/Josa", "는/Josa"])
tfidf = model.fit_transform(reviews)

while True:
    words = input("검색 단어 : ")
    q_tfidf = model.transform([words])
    cos_sim = linear_kernel(q_tfidf, tfidf).flatten()
    idxs = cos_sim.argsort()[:-4:-1] # 상위 3개
    for idx in idxs:
        print(reviews[idx])