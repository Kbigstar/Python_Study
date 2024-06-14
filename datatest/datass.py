import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로드
df = pd.read_csv('ener.csv')

# 날짜 필터 적용
df_filtered = df[(df['ENER_DT'] >= 201401) & (df['ENER_DT'] <= 202312)]

# 각 단지코드 별 평균과 표준편차 계산
grouped = df_filtered.groupby('COMPLEXCODE')['ELEC_USAGE']
mean_std = grouped.agg(['mean', 'std'])

# 표준편차의 2배를 벗어나는 데이터 찾기
def is_outlier(row):
    mean = mean_std.loc[row['COMPLEXCODE']]['mean']
    std = mean_std.loc[row['COMPLEXCODE']]['std']
    return row['ELEC_USAGE'] < (mean - 5 * std) or row['ELEC_USAGE'] > (mean + 5 * std)

# 표준편차 범위를 벗어난 데이터에 대한 boolean 시리즈 생성
outliers = df_filtered.apply(is_outlier, axis=1)

# 표준편차 범위를 벗어난 데이터 출력
outlier_data = df_filtered[outliers]

# 이상치를 포함한 전체 데이터 시각화
plt.figure(figsize=(12, 8))
sns.boxplot(x='COMPLEXCODE', y='ELEC_USAGE', data=df_filtered)
sns.stripplot(x='COMPLEXCODE', y='ELEC_USAGE', data=outlier_data, color='red', jitter=0.4, size=6, marker='o', alpha=0.8)
plt.xticks(rotation=90)
plt.title('Electric Usage by Complex Code with Outliers Marked')
plt.show()
