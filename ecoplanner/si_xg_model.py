import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe') # 1? -> user, 2? -> password, "ip:1521/xe"

# 평가 지표 함수 정의
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# 데이터 로드 및 전처리
def load_and_preprocess_data():
    query = """
        SELECT ener_dt, SUM(ELEC_USAGE) as ELEC_USAGE 
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
    engine = get_engine()
    df = pd.read_sql(query, con=engine)
    df['ener_dt'] = pd.to_datetime(df['ener_dt'], format='%Y%m')
    df['year'] = df['ener_dt'].dt.year
    df['month'] = df['ener_dt'].dt.month
    df.set_index('ener_dt', inplace=True)
    df = df.asfreq('MS')
    df['elec_usage'].fillna(method='ffill', inplace=True)
    return df

# 모델 훈련 및 예측
def train_and_predict_with_xgboost(train_df, test_df):
    X_train = train_df[['year', 'month']]
    y_train = train_df['elec_usage']
    X_test = test_df[['year', 'month']]
    y_test = test_df['elec_usage']

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    forecast_df = pd.DataFrame(y_pred, index=test_df.index, columns=['Forecast'])
    combined_df = test_df.copy()
    combined_df['Forecast'] = forecast_df['Forecast']
    combined_df.dropna(inplace=True)

    return combined_df

# 결과 평가 및 시각화
def evaluate_and_plot_results(train_df, combined_df):
    mse = mean_squared_error(combined_df['elec_usage'], combined_df['Forecast'])
    mae = mean_absolute_error(combined_df['elec_usage'], combined_df['Forecast'])
    rmse = np.sqrt(mean_squared_error(combined_df['elec_usage'], combined_df['Forecast']))
    r2 = r2_score(combined_df['elec_usage'], combined_df['Forecast'])
    mape = mean_absolute_percentage_error(combined_df['elec_usage'], combined_df['Forecast'])

    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'Mean Absolute Percentage Error: {mape}')
    print(f'R-squared: {r2}')

    plt.figure(figsize=(12, 8))
    plt.plot(train_df.index, train_df['elec_usage'], label='Observed (Train)', color='blue')
    plt.plot(combined_df.index, combined_df['elec_usage'], label='Observed (Test)', color='green')
    plt.plot(combined_df.index, combined_df['Forecast'], label='Forecast', color='red')
    plt.xlabel('Date')
    plt.ylabel('Electricity Usage')
    plt.title('XGBoost Forecast of Electricity Usage')
    plt.legend()
    plt.show()

# 메인 실행 코드
df = load_and_preprocess_data()

# 훈련 및 테스트 데이터 분할
train_df = df[df.index.year <= 2022]
test_df = df[df.index.year == 2023]

# 모델 훈련 및 예측
combined_df = train_and_predict_with_xgboost(train_df, test_df)

# 결과 평가 및 시각화
evaluate_and_plot_results(train_df, combined_df)
