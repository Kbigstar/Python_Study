import pandas as pd
from DBManager import DBManager
import numpy as np

# DB 연결
db = DBManager()

# 이미 필터링된 COMPLEXCODE 목록 로드
query_codes = """
SELECT COMPLEXCODE
FROM (
    SELECT COMPLEXCODE, COUNT(DISTINCT SUBSTR(ENER_DT, 1, 6)) as MONTHS_WITH_USAGE
    FROM TMP2
    WHERE TO_NUMBER(SUBSTR(ENER_DT, 1, 6)) BETWEEN 201401 AND 202312
      AND ELEC_USAGE > 0
    GROUP BY COMPLEXCODE
) T
WHERE MONTHS_WITH_USAGE = (
    SELECT COUNT(DISTINCT TO_NUMBER(SUBSTR(ENER_DT, 1, 6)))
    FROM TMP2
    WHERE TO_NUMBER(SUBSTR(ENER_DT, 1, 6)) BETWEEN 201401 AND 202312
)
"""
df_codes = pd.read_sql(query_codes, con=db.conn)
complex_codes = df_codes['COMPLEXCODE'].tolist()

# 각 COMPLEXCODE 별로 ELEC_USAGE와 ELEC_AMOUNT 데이터 조회 및 분석
all_corrected_data = pd.DataFrame()
potential_outliers = pd.DataFrame()

for code in complex_codes:
    query = f"""
    SELECT ENER_DT, ELEC_USAGE, ELEC_AMOUNT
    FROM TMP2
    WHERE COMPLEXCODE = '{code}'
      AND TO_NUMBER(SUBSTR(ENER_DT, 1, 6)) BETWEEN 201401 AND 202312
    """
    df_usage = pd.read_sql(query, con=db.conn)

    # Check if necessary columns exist
    if 'ELEC_USAGE' not in df_usage.columns or 'ELEC_AMOUNT' not in df_usage.columns:
        print(f"Columns 'ELEC_USAGE' or 'ELEC_AMOUNT' not found for COMPLEXCODE {code}")
        continue

    df_usage['YEAR'] = df_usage['ENER_DT'].str[:4]
    df_usage['MONTH'] = df_usage['ENER_DT'].str[4:6]

    # 비율 계산 (ELEC_AMOUNT / ELEC_USAGE)
    df_usage['USAGE_RATE'] = df_usage.apply(lambda row: row['ELEC_AMOUNT'] / row['ELEC_USAGE'] if row['ELEC_USAGE'] > 0 else np.nan, axis=1)

    # 연도별 평균 비율 계산
    yearly_rate = df_usage.groupby('YEAR')['USAGE_RATE'].mean().to_dict()

    # 월별 비율 계산 (특히 7월과 8월)
    monthly_rate = df_usage.groupby(['YEAR', 'MONTH'])['USAGE_RATE'].mean().unstack().to_dict()

    # 이전 해의 마지막 비율을 저장
    previous_year_rate = list(yearly_rate.values())[0]
    previous_july_rate = previous_year_rate
    previous_august_rate = previous_year_rate

    if '07' in monthly_rate:
        previous_july_rate = list(monthly_rate['07'].values())[0]
    if '08' in monthly_rate:
        previous_august_rate = list(monthly_rate['08'].values())[0]

    for idx, row in df_usage.iterrows():
        if row['ELEC_USAGE'] == 0:
            if row['MONTH'] == '07':
                rate = monthly_rate.get('07', {}).get(row['YEAR'], previous_july_rate)
            elif row['MONTH'] == '08':
                rate = monthly_rate.get('08', {}).get(row['YEAR'], previous_august_rate)
            else:
                rate = yearly_rate.get(row['YEAR'], previous_year_rate)
            df_usage.at[idx, 'ELEC_USAGE'] = row['ELEC_AMOUNT'] / rate if rate else 0

            # 잠재적 이상치 저장
            potential_outliers = potential_outliers.append(row, ignore_index=True)

        # 비율 업데이트
        previous_year_rate = yearly_rate.get(row['YEAR'], previous_year_rate)
        if row['MONTH'] == '07':
            previous_july_rate = monthly_rate.get('07', {}).get(row['YEAR'], previous_year_rate)
        if row['MONTH'] == '08':
            previous_august_rate = monthly_rate.get('08', {}).get(row['YEAR'], previous_year_rate)

    # 수정된 데이터 저장
    df_usage['COMPLEXCODE'] = code  # 데이터에 COMPLEXCODE 추가
    all_corrected_data = pd.concat([all_corrected_data, df_usage], ignore_index=True)

# 잠재적 이상치 수동 검토를 위해 출력
print("잠재적 이상치 (수동 검토 필요):")
if not potential_outliers.empty:
    print(potential_outliers[['ENER_DT', 'ELEC_USAGE', 'ELEC_AMOUNT', 'COMPLEXCODE']])
else:
    print("No potential outliers found.")

# 최종 결과 출력 (원본 값, 변경된 값, Z-점수 포함)
outliers_display = all_corrected_data[all_corrected_data['ELEC_USAGE'] == 0]
print("이상치 처리 결과:")
if not outliers_display.empty:
    print(outliers_display[['ENER_DT', 'ELEC_USAGE', 'ELEC_AMOUNT', 'COMPLEXCODE']])
else:
    print("No outliers with ELEC_USAGE == 0 found.")

# 이상치 처리 결과를 CSV 파일로 저장
# outliers_display.to_csv('outliers_display111.csv', index=False)

# 최종 수정된 데이터 저장
# all_corrected_data.to_csv('corrected_elec_usage111.csv', index=False)
