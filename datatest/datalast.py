import pandas as pd
from DBManager import DBManager

# DB 연결
db = DBManager()

# 202301 ~ 202312 기간 동안 elec_usage가 전부 0인 단지코드 조회
query_full_zero_usage = """
SELECT complexcode
FROM tmp2
WHERE TO_NUMBER(SUBSTR(ener_dt, 1, 6)) BETWEEN 202301 AND 202312
  AND elec_usage = 0
GROUP BY complexcode
HAVING COUNT(*) = 12
"""

df_full_zero_usage = pd.read_sql(query_full_zero_usage, con=db.conn)

# 조회된 단지코드의 전체 기간 동안 elec_usage와 elec_amount가 0인 개수를 조회
query_zero_usage_and_amount_count = """
SELECT complexcode, COUNT(*) AS total_zero_usage_and_amount_count
FROM tmp2
WHERE elec_usage = 0 AND elec_amount = 0
GROUP BY complexcode
"""

df_zero_usage_and_amount_count = pd.read_sql(query_zero_usage_and_amount_count, con=db.conn)

# 두 데이터프레임을 합침
df_merged = pd.merge(df_full_zero_usage, df_zero_usage_and_amount_count, on='COMPLEXCODE', how='left')



# 결과 출력
print(df_merged)
