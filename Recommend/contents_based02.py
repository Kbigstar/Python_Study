# 내용기반 추천 Contents based
# 정보검색에서의 Contents based

from sklearn.feature_extraction.text import TfidfVectorizer
from  sklearn.metrics.pairwise import linear_kernel

# TF-IDF
# 단순 키워드 검색에서 보다 의미있는 검색을 위한 방법중 하나.
# TF, Term Frequency (문서 내에서 얼마나 자주 등장하는지)
# IDF, Inverse Document Frequency (문서 집합에서 얼마나 희귀한지)

docs = ["The sky is blue."
        ,"The sun is bright today"
        ,"the sun in the sky is bright"
        ,"We can see the shining sun, the bright sun."]

# tr-idf 모델 생성
model = TfidfVectorizer()
tfidf = model.fit_transform(docs)
print(tfidf)
while True:
    words = input("query words:")
    q_tfidf = model.transform([words])
    cos_sim = linear_kernel(q_tfidf, tfidf).flatten()
    idxs = cos_sim.argsort()[:-4:-1] # 상위 3개
    for idx in idxs:
        print(docs[idx])

