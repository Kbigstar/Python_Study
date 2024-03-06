# pip install gensim
from gensim.models import word2vec
from gensim.models import fasttext

data = word2vec.LineSentence('./naver_movie.nlp')
w_model = word2vec.Word2Vec(data
                            , vector_size=200 # 단어 벡터사이즈
                            , window=8        # 주변 단어 수
                            , min_count=2     # 최소 출현
                            , sg=1)           # 알고리즘 1:skip-gram
f_model = word2vec.Word2Vec(data
                            , vector_size=200 # 단어 벡터사이즈
                            , window=8        # 주변 단어 수
                            , min_count=2     # 최소 출현
                            , sg=1)           # 알고리즘 1:skip-gram

w_model.save("movie_emb.model")
f_model.save("movie_emb_f.model")

while True:
    text = input("검색 단어 : ")
    # positive (가까운 단어), negative (먼 단어)
    print("w_model : ", w_model.wv.most_similar(positive=[text]))
    print("f_model : ", f_model.wv.most_similar(positive=[text]))