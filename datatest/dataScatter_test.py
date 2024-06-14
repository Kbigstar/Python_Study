import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일을 불러옵니다
file_path = 'ener.csv'
data = pd.read_csv(file_path)

# 모든 열에서 0 값을 NaN으로 변환합니다
data.replace(0, np.nan, inplace=True)

# 결측치 확인
missing_values = data.isna().sum()
print("각 열의 결측치 개수:")
print(missing_values)

# ENER_DT를 'YYYYMM' 형식의 문자열로 처리하고 datetime 형식으로 변환합니다
data['ENER_DT'] = pd.to_datetime(data['ENER_DT'].astype(str), format='%Y%m')

# ELEC_USAGE 값이 0인 경우를 카운트합니다 (이제 NA로 변환되었기 때문에 0인 경우는 없습니다)
zero_usage_count = (data['ELEC_USAGE'] == 0).sum()
print(f"ELEC_USAGE 값이 0인 경우의 수: {zero_usage_count}")

# 201401부터 202312까지의 날짜 범위를 생성합니다
full_date_range = pd.date_range(start='2014-01-01', end='2023-12-01', freq='MS')

# 모든 날짜가 각 단지 코드에 포함되도록 데이터를 피벗 테이블로 변환합니다
pivot_table = data.pivot_table(index='ENER_DT', columns='COMPLEXCODE', values='ELEC_USAGE', aggfunc='sum')

# 피벗 테이블을 전체 날짜 범위에 맞추어 재색인하고, 누락된 값을 0으로 채웁니다
pivot_table = pivot_table.reindex(full_date_range, fill_value=0)

# 모든 ELEC_USAGE가 0인 COMPLEXCODE를 찾습니다
zero_usage_complex = pivot_table.columns[(pivot_table == 0).all()].tolist()
zero_usage_complex_count = len(zero_usage_complex)

print(f"모든 ELEC_USAGE 값이 0인 COMPLEXCODE의 수: {zero_usage_complex_count}")
print("모든 ELEC_USAGE 값이 0인 COMPLEXCODE 목록:")
print(zero_usage_complex)

# IQR (사분위 범위)을 계산합니다
elec_usage = data['ELEC_USAGE'].dropna()
Q1 = elec_usage.quantile(0.25)
Q3 = elec_usage.quantile(0.75)
IQR = Q3 - Q1

# 이상치의 범위를 정의합니다
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 데이터에서 이상치를 라벨링합니다
data['Outlier'] = ((data['ELEC_USAGE'] < lower_bound) | (data['ELEC_USAGE'] > upper_bound))
data['Zero'] = data['ELEC_USAGE'].isna()  # 이전에 0이었던 값을 NA로 변환했기 때문에 isna()로 체크

# ELEC_USAGE의 요약 통계를 출력합니다
print("ELEC_USAGE 요약 통계:")
print(data['ELEC_USAGE'].describe())

# 추가 요약 통계 계산
elec_usage_summary = {
    'mean': elec_usage.mean(),
    'median': elec_usage.median(),
    'std_dev': elec_usage.std(),
    'min': elec_usage.min(),
    'max': elec_usage.max(),
    '25%': Q1,
    '50%': elec_usage.median(),
    '75%': Q3,
    'IQR': IQR
}
print("ELEC_USAGE 추가 요약 통계:")
print(elec_usage_summary)

# ELEC_USAGE의 박스 플롯을 그립니다
plt.figure(figsize=(10, 6))
plt.boxplot(elec_usage, vert=False, patch_artist=True)
plt.title('Box Plot of ELEC_USAGE')
plt.xlabel('ELEC_USAGE')
plt.show()

# 로그 변환한 ELEC_USAGE를 추가합니다 (NA 값은 제외)
data['LOG_ELEC_USAGE'] = np.log1p(data['ELEC_USAGE'])

# 각 단지 코드(COMPLEXCODE)별로 월별 Z-점수를 계산하여 이상치 식별
data['Z_Outlier'] = False  # Z-점수 이상치 여부를 저장할 열
data['Month'] = data['ENER_DT'].dt.month  # 월 정보를 추가

# 월별 평균과 표준편차를 저장할 데이터프레임 생성
monthly_stats = []

complex_codes = data['COMPLEXCODE'].unique()
for code in complex_codes:
    for month in range(1, 13):
        df_complex_month = data[(data['COMPLEXCODE'] == code) & (data['Month'] == month) & (data['LOG_ELEC_USAGE'].notna())].copy()
        if df_complex_month.empty:
            continue
        mean_log_usage = df_complex_month['LOG_ELEC_USAGE'].mean()
        std_dev_log_usage = df_complex_month['LOG_ELEC_USAGE'].std()

        # 월별 평균과 표준편차 저장
        monthly_stats.append({
            'COMPLEXCODE': code,
            'Month': month,
            'Mean_LOG_ELEC_USAGE': mean_log_usage,
            'STD_LOG_ELEC_USAGE': std_dev_log_usage
        })

        # Z-점수 계산
        z_scores = (df_complex_month['LOG_ELEC_USAGE'] - mean_log_usage) / std_dev_log_usage
        data.loc[(data['COMPLEXCODE'] == code) & (data['Month'] == month) & (data['LOG_ELEC_USAGE'].notna()), 'z_score'] = z_scores

# 월별 평균과 표준편차 데이터프레임 생성
monthly_stats_df = pd.DataFrame(monthly_stats)

# 월별 평균과 표준편차 출력
print("Monthly Statistics (Mean and STD of LOG_ELEC_USAGE) per COMPLEXCODE and Month:")
print(monthly_stats_df)

# Z-점수가 ±2.5 이상인 경우를 이상치로 라벨링
data['Z_Outlier'] = data['z_score'].abs() >= 2.5

# 이상치와 NA 값을 포함한 데이터
z_outlier_data = data[(data['Z_Outlier']) | (data['ELEC_USAGE'].isna())]

# 'Zero' 열 추가
z_outlier_data.loc[:, 'Zero'] = z_outlier_data['ELEC_USAGE'].isna()

# 'Zero' 값이 False인 데이터만 선택하여 필요한 열을 포함
a = z_outlier_data[z_outlier_data['Zero'] == False][['COMPLEXCODE', 'ENER_DT', 'ELEC_USAGE', 'Z_Outlier', 'z_score', 'LOG_ELEC_USAGE']]
print(a)

# 'LOG_ELEC_USAGE'가 14 이상인 데이터만 선택하여 필요한 열을 포함
b = a[a['LOG_ELEC_USAGE'] >= 14]
print(b)

# b의 ELEC_USAGE 최소값 출력
min_b_elec_usage = b['ELEC_USAGE'].min()
print(f"b의 ELEC_USAGE 최소값: {min_b_elec_usage}")

# 'b' 데이터프레임에 있는 값과 ELEC_USAGE가 NA인 경우만 그리기
plt.figure(figsize=(14, 7))
plt.scatter(b['ENER_DT'], b['ELEC_USAGE'], c='red', alpha=0.5, label='b Data')
plt.scatter(z_outlier_data[z_outlier_data['Zero']]['ENER_DT'], z_outlier_data[z_outlier_data['Zero']]['ELEC_USAGE'], c='green', alpha=0.5, label='Zero ELEC_USAGE')
plt.title('Scatter Plot of ELEC_USAGE with Highlighted Outliers')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE')
plt.legend()
plt.grid(True)
plt.show()
