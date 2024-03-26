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