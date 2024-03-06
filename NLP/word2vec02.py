from gensim.models import FastText
from gensim.models import Word2Vec

f_model = FastText.load('./movie_emb_f.model')
print(f_model.wv.most_similar(positive=["재미", "기생충"], negative=["노잼"]))