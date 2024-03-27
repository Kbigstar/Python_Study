import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import  MultiLabelBinarizer
import numpy as np

rating_data = pd.read_csv("ratings.csv")
movie_data = pd.read_csv("movies.csv")
rating_data.drop('timestamp', axis=1, inplace=True)
movie_data.drop('genres', axis=1, inplace=True)

# 사용자 영화 평점
user_movie_data = pd.merge(rating_data, movie_data, on='movieId')
user_movie_rating = user_movie_data.pivot_table('rating'
                                               , index='userId', columns='title').fillna(0)

# 장르 데이터 (1 ~ n 개 데이터가 | <- 구분자로 구분되어 있음)
movie_data = pd.read_csv('movies.csv')
movie_data['genres'] = movie_data['genres'].apply(lambda x:x.split('|'))
print(movie_data.head())