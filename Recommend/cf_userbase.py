import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# 협업 필터링 - 유저 기반
# 모든 아이템의 동일 차원의 매트릭스 생성

df_ratings = pd.read_csv("ratings.csv")
df_movies = pd.read_csv("movies.csv")
print(df_movies.info())
print(df_ratings.info())

df_ratings.drop('timestamp', axis=1, inplace=True)
print(df_ratings.head())
user_item_rating = pd.merge(df_ratings, df_movies, on='movieId')

user_matrix = user_item_rating.pivot_table("rating", index="userId"
                                           ,columns="title")
user_matrix.fillna(0, inplace=True)
user_cf = cosine_similarity(user_matrix)
result = pd.DataFrame(data=user_cf, index=user_matrix.index
                      ,columns=user_matrix.index)

print(result)
# 대상 유저와 유사한 유저의 평점 높은 영화
def get_user(id, userId):
    movie_arr = user_item_rating[user_item_rating['userId'] == id]
    user_watch_movie = user_item_rating[
                  user_item_rating['userId'] == userId]
    # ~ [제외한다는 의미]
    movie_arr = movie_arr[~movie_arr['movieId'].isin(
        user_watch_movie['movieId'].values.tolist())]
    five_movie = movie_arr.sort_values(by='rating', ascending=False)[:6]
    return five_movie['title'].values.tolist()

    # 가까운 유저
def get_user_item(id):
    best = user_item_rating[
        user_item_rating['userId'] == id].sort_values(
                by='rating', ascending=False)[:5]
    print("my best")
    print(best['title'])
    sim_user = result[id].sort_values(ascending=False)[:6]
    id_arr = sim_user.index.tolist()[1:]
    data = []
    for i in id_arr:
        print("sim user : " + str(i))
        item = get_user(i, id)
        data = data + item
        return  set(data) # 중복이 있을 수 있어서

while True:
    text = input("추천 대상 유저 id : ")
    print(get_user_item(int(text)))
