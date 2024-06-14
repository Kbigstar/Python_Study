import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from itertools import product

# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe') # 1? -> user, 2? -> password, "ip:1521/xe"

# 최적의 SARIMAX 파라미터 탐색 함수
def find_best_sarimax_params(train_df, exog_train):
    p = d = q = range(0, 3)
    pdq = list(product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

    best_aic = np.inf
    best_params = None

    for param in pdq:
        for seasonal_param in seasonal_pdq:
            try:
                model = SARIMAX(train_df['elec_usage'], order=param, seasonal_order=seasonal_param, exog=exog_train)
                model_fit = model.fit(disp=False)
                if model_fit.aic < best_aic:
                    best_aic = model_fit.aic
                    best_params = (param, seasonal_param)
            except Exception as e:
                continue

    return best_params

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

    # 로그 변환
    df['elec_usage'] = np.log(df['elec_usage'])

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

    # 최적의 SARIMAX 파라미터 찾기
    best_params = find_best_sarimax_params(train_df, exog_train)
    if best_params is None:
        print("No suitable parameters found.")
        return
    order, seasonal_order = best_params

    # 최적의 SARIMAX 모델 적합
    model = SARIMAX(train_df['elec_usage'], order=order, seasonal_order=seasonal_order, exog=exog_train)
    model_fit = model.fit(disp=False)

    # 수렴 문제 또는 기타 경고 확인
    print(model_fit.summary())

    # 예측 수행
    forecast_steps = len(test_df)
    forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_test)
    forecast_values = forecast.predicted_mean

    # Ensure forecast_values is not NaN
    if forecast_values.isnull().any():
        print("NaN values found in forecast.")
        return

    # 역변환 (로그 변환의 반대)
    forecast_values = np.exp(forecast_values)

    # Create DataFrame from forecast values
    forecast_df = pd.DataFrame(forecast_values, index=test_df.index, columns=['Forecast'])
    print("Forecast DataFrame:\n", forecast_df)

    # 실제 테스트 데이터와 예측 데이터 결합
    combined_df = test_df.copy()
    combined_df['Forecast'] = forecast_df['Forecast']

    # 역변환 (로그 변환의 반대)
    combined_df['elec_usage'] = np.exp(combined_df['elec_usage'])

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

# 테스트를 위해 complexcode 'A30005002' 사용
create_and_evaluate_model('A30005002')