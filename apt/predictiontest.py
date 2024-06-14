import pandas as pd
import cx_Oracle
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np  # numpy 추가

# Oracle 데이터베이스에 연결
conn = cx_Oracle.connect("study", "study", "localhost:1521/xe")

# ex_energy 테이블과 ex_apartment 테이블에서 데이터 가져오기
query = """
    SELECT e.elec_energy AS ELEC_ENERGY, e.energy AS ENERGY, a.apart_buildingnm AS APART_BUILDINGNM
    FROM ex_energy e
    JOIN ex_apartment a ON e.complexcode = a.aprat_complexcode
    WHERE e.energy BETWEEN '201401' AND '202312'
    AND a.aprat_complexcode = 'A30275104'
"""
df = pd.read_sql(query, con=conn)

# 데이터 프레임을 시계열 데이터로 변환
df['ENERGY'] = pd.to_datetime(df['ENERGY'], format='%Y%m')

df.set_index('ENERGY', inplace=True)
df.sort_index(inplace=True)

# 월별로 데이터를 합산하여 전력 사용량을 계산합니다.
df = df.resample('M').sum()

# ARIMA 모델 학습
model = ARIMA(df['ELEC_ENERGY'], order=(5,1,0))  # ARIMA 모델의 파라미터는 예시로 (p, d, q)를 사용했습니다.
result = model.fit()

# 2024년 1월 데이터 생성
future_dates = pd.date_range(start=df.index[-1], periods=1, freq='M')

# 예측
forecast = result.predict(start=future_dates[0], end=future_dates[-1], typ='levels')

# 결과 출력
print(forecast)

# 실제값과 예측값을 numpy 배열로 변환
y_true = df['ELEC_ENERGY'].iloc[-1:].values.repeat(len(forecast))  # 예측값과 동일한 길이로 만듦

# 예측값을 정수로 변환하여 소수점 이하를 없앰
forecast_int = forecast.astype(int)

# RMSE 계산
rmse = np.sqrt(mean_squared_error(y_true, forecast_int))

print('RMSE:', rmse)

# 연결 닫기
conn.close()
    