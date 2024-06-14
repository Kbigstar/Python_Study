import pandas as pd
from DBManager import DBManager
import numpy as np

# DB 연결
db = DBManager()

# 이미 필터링된 complexcode 목록 로드
query_codes = """
SELECT DISTINCT complexcode
FROM tmp2
WHERE TO_NUMBER(SUBSTR(ener_dt, 1, 6)) BETWEEN 201401 AND 202312
  AND elec_usage > 0
"""
df_codes = pd.read_sql(query_codes, con=db.conn)
complex_codes = df_codes['COMPLEXCODE'].tolist()

# 각 complexcode 별 이상치 결과를 저장할 DataFrame
outliers_all = pd.DataFrame()

# 각 complexcode 별로 elec_usage 데이터 분석 및 이상치 식별
for code in complex_codes:
    query = f"""
    SELECT ener_dt, elec_usage
    FROM tmp2
    WHERE complexcode = '{code}'
      AND TO_NUMBER(SUBSTR(ener_dt, 1, 6)) BETWEEN 201401 AND 202312
      AND elec_usage > 0
    """
    df_usage = pd.read_sql(query, con=db.conn)
    df_usage['month'] = df_usage['ENER_DT'].str[4:6]  # 'ener_dt'에서 월 정보 추출

    # 월별로 그룹화하여 평균과 표준편차 계산
    for month in df_usage['month'].unique():
        df_month = df_usage[df_usage['month'] == month]
        mean_usage = df_month['ELEC_USAGE'].mean()
        std_dev_usage = df_month['ELEC_USAGE'].std()

        # 이상치 식별 (평균 ± 2 표준편차를 벗어나는 경우)
        df_month['is_outlier'] = df_month['ELEC_USAGE'].apply(lambda x: abs(x - mean_usage) > 2 * std_dev_usage)

        # 이상치만 필터링하여 추가
        outliers = df_month[df_month['is_outlier']]
        outliers['COMPLEXCODE'] = code  # 이상치 데이터에 complexcode 추가
        outliers_all = pd.concat([outliers_all, outliers], ignore_index=True)

# 결과 출력
print(outliers_all)
