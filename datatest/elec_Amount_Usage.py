import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# CSV 파일을 불러옵니다
file_path = 'ener.csv'
data = pd.read_csv(file_path)

# ENER_DT를 'YYYYMM' 형식의 문자열로 처리하고 datetime 형식으로 변환합니다
data['ENER_DT'] = pd.to_datetime(data['ENER_DT'].astype(str), format='%Y%m')

# ELEC_USAGE 값이 0인 경우를 카운트합니다
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
data['Zero'] = data['ELEC_USAGE'] == 0

# ELEC_USAGE의 박스 플롯을 그립니다
plt.figure(figsize=(10, 6))
plt.boxplot(elec_usage, vert=False, patch_artist=True)
plt.title('Box Plot of ELEC_USAGE')
plt.xlabel('ELEC_USAGE')
plt.show()

# 로그 변환한 ELEC_USAGE를 추가합니다 (0 값은 제외)
data['LOG_ELEC_USAGE'] = np.log1p(data['ELEC_USAGE'].replace(0, np.nan))

# ELEC_USAGE의 로그 변환 히스토그램을 그립니다
plt.figure(figsize=(10, 6))
sns.histplot(data['LOG_ELEC_USAGE'].dropna(), bins=50, kde=True)
plt.title('Log-Transformed Histogram of ELEC_USAGE')
plt.xlabel('Log of ELEC_USAGE')
plt.ylabel('Frequency')
plt.show()

# ELEC_USAGE의 타임 시리즈 플롯을 그립니다
plt.figure(figsize=(14, 7))
plt.plot(data['ENER_DT'], data['ELEC_USAGE'], marker='o', linestyle='-')
plt.title('Time Series of ELEC_USAGE')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE')
plt.grid(True)
plt.show()

# ELEC_AMOUNT와 ELEC_USAGE의 상관관계 히트맵을 그립니다
plt.figure(figsize=(10, 8))
correlation_matrix = data[['ELEC_AMOUNT', 'ELEC_USAGE']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation between ELEC_AMOUNT and ELEC_USAGE')
plt.show()

# 로그 변환한 ELEC_AMOUNT와 ELEC_USAGE의 산점도를 그립니다
plt.figure(figsize=(10, 6))
log_elec_amount = np.log1p(data['ELEC_AMOUNT'])
sns.scatterplot(x=log_elec_amount, y=data['LOG_ELEC_USAGE'], data=data)
plt.title('Log-Transformed Scatter Plot of ELEC_AMOUNT vs ELEC_USAGE')
plt.xlabel('Log of ELEC_AMOUNT')
plt.ylabel('Log of ELEC_USAGE')
plt.show()

# 로그 변환한 ELEC_AMOUNT와 ELEC_USAGE의 상관관계를 계산합니다
log_corr = np.log1p(data[['ELEC_AMOUNT', 'ELEC_USAGE']]).corr()
print("로그 변환된 ELEC_AMOUNT와 ELEC_USAGE의 상관관계:")
print(log_corr)

# 이상치가 있는 행을 출력합니다
outliers = data[data['Outlier'] | data['Zero']]
outliers_display = outliers[['COMPLEXCODE', 'ENER_DT', 'ELEC_USAGE', 'Outlier', 'Zero']]
print(outliers_display)

# 0과 이상치를 색깔로 구분하여 시각화
plt.figure(figsize=(14, 7))
colors = np.where(data['ELEC_USAGE'] == 0, 'blue', np.where(data['ELEC_USAGE'] >= 3000000, 'red', 'green'))
plt.scatter(data['ENER_DT'], data['ELEC_USAGE'], c=colors, alpha=0.5)
plt.title('Scatter Plot of ELEC_USAGE with Outliers and Zero Values Highlighted')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE')
plt.grid(True)
plt.show()
print(f"전체 데이터 개수: {len(data)}")

# 기존 코드 (이상치가 아닌 값은 포함하지 않음)
plt.figure(figsize=(14, 7))
outlier_data = data[data['Outlier'] | data['Zero']]
colors = np.where(outlier_data['ELEC_USAGE'] == 0, 'blue', 'red')
plt.scatter(outlier_data['ENER_DT'], outlier_data['ELEC_USAGE'], c=colors, alpha=0.5)
plt.title('Scatter Plot of ELEC_USAGE with Outliers and Zero Values Highlighted')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE')
plt.grid(True)
plt.show()
print(f"이상치와 0값 데이터 개수: {len(outlier_data)}")

# 이상치 개수
outlier_count = data['Outlier'].sum()
print(f"이상치 데이터 개수: {outlier_count}")

# ELEC_USAGE 값이 0인 데이터 개수
zero_count = data['Zero'].sum()
print(f"ELEC_USAGE 값이 0인 데이터 개수: {zero_count}")

# 이상치와 0값이 겹치는 데이터 개수
overlap_count = data[(data['Outlier']) & (data['Zero'])].shape[0]
print(f"이상치와 0값이 겹치는 데이터 개수: {overlap_count}")

# 각 단지 코드(COMPLEXCODE)별로 월별 Z-점수를 계산하여 이상치 식별
data['Z_Outlier'] = False  # Z-점수 이상치 여부를 저장할 열
data['Month'] = data['ENER_DT'].dt.month  # 월 정보를 추가

complex_codes = data['COMPLEXCODE'].unique()
for code in complex_codes:
    for month in range(1, 13):
        df_complex_month = data[(data['COMPLEXCODE'] == code) & (data['Month'] == month)].copy()
        if df_complex_month.empty:
            continue
        mean_log_usage = df_complex_month['LOG_ELEC_USAGE'].mean()
        std_dev_log_usage = df_complex_month['LOG_ELEC_USAGE'].std()

        # Z-점수 계산
        z_scores = (df_complex_month['LOG_ELEC_USAGE'] - mean_log_usage) / std_dev_log_usage
        data.loc[(data['COMPLEXCODE'] == code) & (data['Month'] == month), 'z_score'] = z_scores

# Z-점수가 ±2.5 이상인 경우를 이상치로 라벨링
data['Z_Outlier'] = data['z_score'].abs() >= 2.5

# 이상치와 0 값을 포함한 데이터
z_outlier_data = data[(data['Z_Outlier']) | (data['ELEC_USAGE'] == 0)]

# 'Zero' 열 추가
z_outlier_data['Zero'] = z_outlier_data['ELEC_USAGE'] == 0

# 'Zero' 값이 False인 데이터만 선택하여 필요한 열을 포함
a = z_outlier_data[z_outlier_data['Zero'] == False][['COMPLEXCODE', 'ENER_DT', 'ELEC_USAGE', 'Z_Outlier', 'z_score', 'LOG_ELEC_USAGE']]
print(a)

# 'LOG_ELEC_USAGE'가 14 이상인 데이터만 선택하여 필요한 열을 포함
b = a[a['LOG_ELEC_USAGE'] >= 14]
print(b)

