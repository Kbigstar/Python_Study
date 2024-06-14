import pandas as pd
from DBManager import DBManager
from scipy.stats import zscore

# DB 연결
db = DBManager()

# ENERGY 테이블에서 모든 데이터를 조회
query_all_data = """
SELECT COMPLEXCODE, ENER_DT, ELEC_USAGE
FROM ENERGY
WHERE TO_NUMBER(SUBSTR(ENER_DT, 1, 6)) BETWEEN 201401 AND 202312
AND ELEC_USAGE != 0
"""
df_all_data = pd.read_sql(query_all_data, con=db.conn)

# 각 complexcode 별로 z-score 계산
df_all_data['Z_SCORE'] = df_all_data.groupby('COMPLEXCODE')['ELEC_USAGE'].transform(lambda x: zscore(x, ddof=0))

# z-score가 3 이상인 데이터만 필터링
df_3sigma = df_all_data[df_all_data['Z_SCORE'] >= 2.5]

# z-score가 높은 순으로 정렬
df_sorted = df_3sigma.sort_values(by='Z_SCORE', ascending=False)

# 결과 출력
print("Z-Score가 3 이상인 데이터:")
print(df_sorted)

db.conn.close()
