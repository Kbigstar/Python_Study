import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe')# 1? -> user, 2? -> password, "ip:1521/xe"

# 단지 코드 기반 모델 생성 및 평가 함수
def create_and_evaluate_model(complexcode):
    query = f"""
        SELECT ENER_DT, SUM(ELEC_USAGE) as ELEC_USAGE
        FROM TMP2
        WHERE complexcode = '{complexcode}'
        AND TO_NUMBER(TO_CHAR(TO_DATE(ENER_DT, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
        GROUP BY ENER_DT
        ORDER BY ENER_DT
    """

    # 데이터베이스 연결 및 데이터 로드
    engine = get_engine()
    df = pd.read_sql(query, con=engine)

    # 데이터 전처리
    df['ener_dt'] = pd.to_datetime(df['ener_dt'], format='%Y%m')
    df.set_index('ener_dt', inplace=True)
    df = df.asfreq('MS')

    # 결측값 확인 및 처리
    df['elec_usage'] = df['elec_usage'].ffill()  # 결측값을 전방 채움 방식으로 처리

    # 훈련 및 테스트 데이터 분할
    train_df = df[df.index.year <= 2022]
    test_df = df[df.index.year == 2023]

    # 외생 변수 준비
    exog_train = pd.DataFrame({
        'year': train_df.index.year,
        'month': train_df.index.month
    }, index=train_df.index)
    exog_test = pd.DataFrame({
        'year': test_df.index.year,
        'month': test_df.index.month
    }, index=test_df.index)

    # SARIMAX 모델 적합
    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)
    model = SARIMAX(train_df['elec_usage'], order=order, seasonal_order=seasonal_order, exog=exog_train)
    model_fit = model.fit(disp=False, maxiter=1000, method='nm')

    # 수렴 문제 또는 기타 경고 확인
    print(model_fit.summary())

    # 예측 수행
    forecast_steps = len(test_df)
    forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_test)
    forecast_values = forecast.predicted_mean

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

    # 예측 정확도를 평가하기 위한 지표 계산 및 출력
    combined_df.dropna(inplace=True)
    mse = mean_squared_error(combined_df['elec_usage'], combined_df['Forecast'])
    mae = mean_absolute_error(combined_df['elec_usage'], combined_df['Forecast'])
    rmse = np.sqrt(mean_squared_error(combined_df['elec_usage'], combined_df['Forecast']))
    r2 = r2_score(combined_df['elec_usage'], combined_df['Forecast'])

    def mean_absolute_percentage_error(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    mape = mean_absolute_percentage_error(combined_df['elec_usage'], combined_df['Forecast'])

    def mean_bias_deviation(y_true, y_pred):
        return np.mean(y_pred - y_true)

    mbd = mean_bias_deviation(combined_df['elec_usage'], combined_df['Forecast'])

    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'Mean Absolute Percentage Error: {mape}')
    print(f'R-squared: {r2}')
    print(f'Mean Bias Deviation: {mbd}')

    # 그래프 시각화
    plt.figure(figsize=(14, 7))
    plt.plot(train_df.index, train_df['elec_usage'], label='Train Data', color='blue')
    plt.plot(test_df.index, test_df['elec_usage'], label='Test Data', color='green')
    plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red')
    plt.xlabel('Date')
    plt.ylabel('Electricity Usage')
    plt.title('Electricity Usage Forecast')
    plt.legend()
    plt.show()

# 테스트를 위해 complexcode 'A30005002' 사용
create_and_evaluate_model('A30005002')
