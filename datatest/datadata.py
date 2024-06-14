import pandas as pd
from DBManager import DBManager

db = DBManager()
query = """
SELECT complexcode
FROM tmp2
WHERE TO_NUMBER(TO_CHAR(TO_DATE(ener_dt, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
GROUP BY complexcode
HAVING COUNT(*) = COUNT(CASE WHEN elec_usage = 0 THEN 1 ELSE NULL END)
       AND COUNT(*) = (2023 - 2014 + 1) * 12
"""
df_full_zero_usage = pd.read_sql(query, con=db.conn)

# 인덱스를 1부터 시작하도록 조정
df_full_zero_usage.index = range(1, len(df_full_zero_usage) + 1)

print(df_full_zero_usage)
