import pandas as pd

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
print(outlier_data)