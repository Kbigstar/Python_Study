import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima

# 데이터 로드 및 처리
data = {
    "ENER_DT": ["2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12", "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10"],
    "ELEC_USAGE": [290, 300, 325, 315, 305, 372, 440, 500, 388, 359, 327, 312, 320, 310, 400, 350, 420, 410, 450, 430, 380, 390]
}
df = pd.DataFrame(data)
df['ENER_DT'] = pd.to_datetime(df['ENER_DT'], format='%Y-%m')
df.set_index('ENER_DT', inplace=True)

# 시계열 데이터 시각화
df['ELEC_USAGE'].plot(figsize=(10, 5))
plt.title('Monthly Electricity Usage')
plt.xlabel('Date')
plt.ylabel('Electricity Usage')
plt.show()

# SARIMA 모델 훈련
sarima_model = auto_arima(df['ELEC_USAGE'], seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True)

# 모델 요약
print(sarima_model.summary())

# 다음 달 전기 사용량 예측
forecast = sarima_model.predict(n_periods=1)
print(f"Forecast for next month's electricity usage: {forecast[0]}")
