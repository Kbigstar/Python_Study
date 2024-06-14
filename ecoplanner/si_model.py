import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.font_manager as fm
from matplotlib import rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 폰트 경로
font_name = fm.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe') # 1? -> user, 2? -> password, "ip:1521/xe"

# Step 1: 필요한 라이브러리 임포트
engine = get_engine()

# Step 2: 데이터 로드 (실제 데이터 로드로 교체)
query = """
    SELECT ener_dt, SUM(ELEC_USAGE) as elec_usage 
    FROM TMP2 a, APT_SIZE b
    WHERE a.complexcode = b.apart_complexcode
    AND a.complexcode IN (
        SELECT COMPLEXCODE
        FROM TMP2
        WHERE TO_NUMBER(TO_CHAR(TO_DATE(ener_dt, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
        GROUP BY COMPLEXCODE
        HAVING COUNT(CASE WHEN ELEC_USAGE = 0 THEN 1 ELSE NULL END) = 0
    )   
    GROUP BY ener_dt
    ORDER BY ener_dt
"""
df = pd.read_sql(query, con=engine)

# Step 3: 데이터 전처리
df['ener_dt'] = pd.to_datetime(df['ener_dt'], format='%Y%m')
df['year'] = df['ener_dt'].dt.year
df['month'] = df['ener_dt'].dt.month
df.set_index('ener_dt', inplace=True)
df = df.asfreq('MS')  # 월별 빈도 설정

# 결측값 확인 및 처리
print("Missing values in dataset:", df.isnull().sum())
df['elec_usage'] = df['elec_usage'].ffill()  # 결측값을 전방 채움 방식으로 처리

# 훈련 및 테스트 데이터 분할
train_df = df[df.index.year <= 2022]
test_df = df[df.index.year == 2023]

# 외생 변수 준비
exog_train = train_df[['year', 'month']]
exog_test = test_df[['year', 'month']]

# 데이터프레임의 크기 확인 (디버깅용)
print(f"Train Data Shape: {train_df.shape}")
print(f"Test Data Shape: {test_df.shape}")

# 훈련 데이터의 결측값 확인
print("Missing values in training data:", train_df.isnull().sum())

# Step 4: SARIMAX 모델 훈련
# 모델의 순서 및 계절 순서 정의
order = (1, 1, 1)
seasonal_order = (1, 1, 1, 12)

# SARIMAX 모델 적합 (외생 변수 포함)
model = SARIMAX(train_df['elec_usage'], order=order, seasonal_order=seasonal_order, exog=exog_train)
model_fit = model.fit(disp=False, maxiter=1000, method='nm')

# 수렴 문제 또는 기타 경고 확인
print(model_fit.summary())

# Step 5: 예측 수행
forecast_steps = len(test_df)  # 예측 단계는 테스트 세트의 길이와 일치해야 함
print("Exogenous variables for prediction:\n", exog_test)
forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_test)
forecast_values = forecast.predicted_mean
print("Forecast values:\n", forecast_values)

# Ensure forecast_values is not NaN
print("Any NaN in forecast values:", forecast_values.isnull().any())

# Extract values from forecast series
forecast_values_only = forecast_values.values
# Create DataFrame from forecast values
forecast_df = pd.DataFrame(forecast_values_only, index=test_df.index, columns=['Forecast'])
print("Forecast DataFrame:\n", forecast_df)

# 실제 테스트 데이터와 예측 데이터 결합
combined_df = test_df.copy()
combined_df['Forecast'] = forecast_df['Forecast']

# 예측값의 결측값 확인
print("Missing values in forecast:", forecast_df.isnull().sum())
print("Combined DataFrame:\n", combined_df)

# 결과 그래프 출력
plt.figure(figsize=(12, 8))
plt.plot(train_df.index, train_df['elec_usage'], label='Observed (Train)', color='blue')
plt.plot(test_df.index, test_df['elec_usage'], label='Observed (Test)', color='green')
plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red')
plt.xlabel('Date')
plt.ylabel('Electricity Usage')
plt.title('대전광역시 전력량 예측 [SARIMAX]')
plt.legend()
plt.show()

# 예측 정확도 평가를 위한 지표 계산
mse = mean_squared_error(combined_df['elec_usage'], combined_df['Forecast'])
mae = mean_absolute_error(combined_df['elec_usage'], combined_df['Forecast'])
rmse = np.sqrt(mse)
r2 = r2_score(combined_df['elec_usage'], combined_df['Forecast'])

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape = mean_absolute_percentage_error(combined_df['elec_usage'], combined_df['Forecast'])

def mean_bias_deviation(y_true, y_pred):
    return np.mean(y_pred - y_true)

mbd = mean_bias_deviation(combined_df['elec_usage'], combined_df['Forecast'])

# 평가 지표 출력
print(f'Mean Squared Error: {mse:.4f}')
print(f'Mean Absolute Error: {mae:.4f}')
print(f'Root Mean Squared Error: {rmse:.4f}')
print(f'Mean Absolute Percentage Error: {mape:.4f}%')
print(f'R-squared: {r2:.4f}')
print(f'Mean Bias Deviation: {mbd:.4f}')
