from DBManager import DBManager
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

sql_user = """ 
    SELECT a.email
          ,a.nick_name
          ,b.q_id
          ,b.select_option
    FROM tb_user a
        ,tb_response b
    WHERE a.email = b.email
 """

db = DBManager()
df = pd.read_sql(con=db.conn, sql=sql_user)
option_mapping = {'A':0, 'B':1, 'N':0.5}
df['SELECT_VALUE'] = df['SELECT_OPTION'].map(option_mapping)
print(df.head())

matrix = df.pivot_table(index='EMAIL', columns='Q_ID', values='SELECT_VALUE')
sim_matrix = cosine_similarity(matrix)
print(sim_matrix)

sim_df = pd.DataFrame(sim_matrix, index=matrix.index, columns=matrix.index)
print(sim_df.head())

target_user = '127897@naver.com'
# 해당 사용자의 유사도
target_user_sim = sim_df[target_user]
# 자신 제외하고 유사도 높은 순으로 정렬
sorted_sim = target_user_sim.drop(target_user).sort_values(ascending=False)

#결과 출력
print(target_user + ' 사용자와 유사한 사용자 순서')
print(sorted_sim.reset_index().values.tolist())