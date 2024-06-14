import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 폰트 경로
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())

# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe') # 1? -> user, 2? -> password, "ip:1521/xe"


# 필요한 평가 지표 함수 정의
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# 구별 모델 생성 및 평가 함수
def create_and_evaluate_model(district):
    query = f"""
        SELECT ENER_DT, SUM(ELEC_USAGE) as ELEC_USAGE
        FROM TMP2 a, APT_SIZE b
        WHERE a.complexcode = b.apart_complexcode
        AND a.complexcode IN (
            SELECT COMPLEXCODE
            FROM TMP2
            WHERE TO_NUMBER(TO_CHAR(TO_DATE(ENER_DT, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
            GROUP BY COMPLEXCODE
            HAVING COUNT(CASE WHEN ELEC_USAGE = 0 THEN 1 ELSE NULL END) = 0
        )   
        AND SIZE_DISTRICT = '{district}'
        GROUP BY ENER_DT
        ORDER BY 1
    """

    # 데이터베이스 연결 및 데이터 로드
    engine = get_engine()
    df = pd.read_sql(query, con=engine)

    # 데이터 전처리
    df['ener_dt'] = pd.to_datetime(df['ener_dt'], format='%Y%m')
    df.set_index('ener_dt', inplace=True)
    df = df.asfreq('MS')



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
    model_fit = model.fit(disp=False)

    # 예측 수행
    forecast_steps = len(test_df)
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
    combined_df.dropna(inplace=True)

    # 평가 지표 계산
    mse = mean_squared_error(combined_df['elec_usage'], combined_df['Forecast'])
    mae = mean_absolute_error(combined_df['elec_usage'], combined_df['Forecast'])
    rmse = np.sqrt(mean_squared_error(combined_df['elec_usage'], combined_df['Forecast']))
    r2 = r2_score(combined_df['elec_usage'], combined_df['Forecast'])
    mape = mean_absolute_percentage_error(combined_df['elec_usage'], combined_df['Forecast'])

    print(f'Evaluation for district: {district}')
    print(f'Mean Squared Error: {mse:.4f}')
    print(f'Mean Absolute Error: {mae:.4f}')
    print(f'Root Mean Squared Error: {rmse:.4f}')
    print(f'Mean Absolute Percentage Error: {mape:.4f}%')
    print(f'R-squared: {r2:.4f}')


    # 결과 그래프 출력
    plt.figure(figsize=(12, 8))
    plt.plot(train_df.index, train_df['elec_usage'], label='Observed (Train)', color='blue')
    plt.plot(test_df.index, test_df['elec_usage'], label='Observed (Test)', color='green')
    plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red')
    plt.xlabel('Date')
    plt.ylabel('Electricity Usage')
    plt.title(f'SARIMAX Forecast of Electricity Usage for {district}')
    plt.legend()
    plt.show()

# 각 구별로 모델 생성 및 평가
districts = ['대덕구', '중구', '서구','유성구','동구']
for district in districts:
    create_and_evaluate_model(district)