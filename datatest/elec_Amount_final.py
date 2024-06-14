import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

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

# 월 변수 추가
data['MONTH'] = data['ENER_DT'].dt.month

# ELEC_AMOUNT와 ELEC_USAGE의 로그 변환
data['LOG_ELEC_USAGE'] = np.log1p(data['ELEC_USAGE'])
data['LOG_ELEC_AMOUNT'] = np.log1p(data['ELEC_AMOUNT'])
data['YEAR'] = data['ENER_DT'].dt.year

# 상관관계 확인
correlation = data[['LOG_ELEC_USAGE', 'LOG_ELEC_AMOUNT']].corr()
print("로그 변환된 ELEC_AMOUNT와 ELEC_USAGE의 상관관계:")
print(correlation)

# ELEC_USAGE_IMPUTED 열 초기화
data['ELEC_USAGE_IMPUTED'] = data['ELEC_USAGE']

# 결측치를 예측하여 채우기
for year in data['YEAR'].unique():
    year_data = data[data['YEAR'] == year]
    non_missing_data = year_data.dropna(subset=['LOG_ELEC_USAGE', 'LOG_ELEC_AMOUNT'])
    missing_data = year_data[year_data['LOG_ELEC_USAGE'].isna() & year_data['LOG_ELEC_AMOUNT'].notna()]

    if not non_missing_data.empty:
        # 회귀 분석을 수행하여 모델을 학습시킵니다
        X_train = non_missing_data[['LOG_ELEC_AMOUNT', 'MONTH']]
        y_train = non_missing_data['LOG_ELEC_USAGE']

        model = GradientBoostingRegressor()
        model.fit(X_train, y_train)

        # 평가
        y_train_pred = model.predict(X_train)
        r2 = r2_score(y_train, y_train_pred)
        mse = mean_squared_error(y_train, y_train_pred)
        mae = mean_absolute_error(y_train, y_train_pred)

        print(f"Year: {year}, R²: {r2:.4f}, MSE: {mse:.4f}, MAE: {mae:.4f}")

        if not missing_data.empty:
            # 결측치가 있는 데이터의 LOG_ELEC_AMOUNT도 평균값으로 대체
            X_missing = missing_data[['LOG_ELEC_AMOUNT', 'MONTH']]

            # 회귀 모델을 사용하여 결측치를 예측합니다
            predicted_usage = model.predict(X_missing)

            # 예측된 값을 대체합니다
            indices_to_update = (data['YEAR'] == year) & (data['LOG_ELEC_USAGE'].isna()) & (data['LOG_ELEC_AMOUNT'].notna())
            data.loc[indices_to_update, 'LOG_ELEC_USAGE'] = predicted_usage
            data.loc[indices_to_update, 'ELEC_USAGE_IMPUTED'] = np.expm1(predicted_usage)

# ELEC_AMOUNT와 ELEC_USAGE가 둘 다 NaN인 경우 대체하지 않은 데이터 유지
data['ELEC_USAGE_IMPUTED'] = np.where(data['ELEC_AMOUNT'].isna() & data['ELEC_USAGE'].isna(), np.nan, data['ELEC_USAGE_IMPUTED'])

# 로그 변환된 ELEC_USAGE가 14 이상인 경우 처리
high_log_indices = data['LOG_ELEC_USAGE'] >= 14
high_log_data = data[high_log_indices]

# 평균 대체를 위한 작업
for index, row in high_log_data.iterrows():
    complexcode = row['COMPLEXCODE']
    month = row['MONTH']

    if row['ELEC_AMOUNT'] < 100000:
        # 해당 complexcode의 해당 월의 평균 elec_usage 구하기 (현재 연도 제외)
        mean_usage = data[(data['COMPLEXCODE'] == complexcode) &
                          (data['MONTH'] == month) &
                          (data['ELEC_AMOUNT'] >= 100000)]['ELEC_USAGE'].mean()

        if not np.isnan(mean_usage):
            data.at[index, 'ELEC_USAGE_IMPUTED'] = mean_usage
    else:
        # 예측된 값을 대체
        log_elec_amount = row['LOG_ELEC_AMOUNT']
        month = row['MONTH']
        X_predict = pd.DataFrame({'LOG_ELEC_AMOUNT': [log_elec_amount], 'MONTH': [month]})
        predicted_usage = model.predict(X_predict)
        data.at[index, 'ELEC_USAGE_IMPUTED'] = np.expm1(predicted_usage)

# 대체 전후 값을 포함하는 데이터프레임 생성
result_df = data[['COMPLEXCODE', 'ENER_DT', 'ELEC_AMOUNT', 'ELEC_USAGE', 'ELEC_USAGE_IMPUTED', 'YEAR']].copy()
result_df.columns = ['COMPLEXCODE', 'ENER_DT', 'ELEC_AMOUNT', 'ELEC_USAGE_BEFORE', 'ELEC_USAGE_AFTER', 'YEAR']

# ELEC_AMOUNT와 ELEC_USAGE가 둘 다 NaN인 행 제거
result_df = result_df.dropna(subset=['ELEC_AMOUNT', 'ELEC_USAGE_BEFORE'], how='all')

# ELEC_AMOUNT 대비 ELEC_USAGE 비율 계산
result_df['USAGE_RATE_BEFORE'] = result_df['ELEC_USAGE_BEFORE'] / result_df['ELEC_AMOUNT']
result_df['USAGE_RATE_AFTER'] = result_df['ELEC_USAGE_AFTER'] / result_df['ELEC_AMOUNT']

# 결과 출력
print(result_df)

# 로그 변환된 ELEC_USAGE가 14 이상인 데이터 출력
high_log_elec_usage_result = result_df[data['LOG_ELEC_USAGE'] >= 14]
print("로그 변환된 ELEC_USAGE가 14 이상인 데이터:")
print(high_log_elec_usage_result)

# 비율이 큰 값들 확인
outliers = result_df[
    result_df['USAGE_RATE_AFTER'] > result_df['USAGE_RATE_AFTER'].mean() + 2 * result_df['USAGE_RATE_AFTER'].std()]
print("비율이 큰 값들:")
print(outliers)

# 비율이 큰 값을 시각화
plt.figure(figsize=(14, 7))
plt.scatter(result_df['ENER_DT'], result_df['USAGE_RATE_AFTER'], color='red', label='USAGE_RATE_AFTER')
plt.scatter(result_df['ENER_DT'], result_df['USAGE_RATE_BEFORE'], color='blue', label='USAGE_RATE_BEFORE')
plt.axhline(y=result_df['USAGE_RATE_AFTER'].mean() + 2 * result_df['USAGE_RATE_AFTER'].std(), color='green',
            linestyle='--', label='Outlier Threshold')
plt.title('ELEC_USAGE_RATE Before and After Imputation')
plt.xlabel('Date')
plt.ylabel('Usage Rate')
plt.legend()
plt.grid(True)
plt.show()

# # CSV 파일로 저장
# file_name = 'complex_elec_usage_comparison_final.csv'
# result_df.to_csv(file_name, index=False)
# print(f"Saved {file_name}")

# 로그 변환된 ELEC_USAGE가 14 이상인 데이터를 별도 CSV 파일로 저장
high_log_elec_usage_file = '6high_log_elec_usage.csv'
high_log_elec_usage_result.to_csv(high_log_elec_usage_file, index=False)
print(f"Saved {high_log_elec_usage_file}")
