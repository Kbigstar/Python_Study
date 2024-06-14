import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 시스템에 설치된 한글 폰트 경로
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
    df['year'] = df['ener_dt'].dt.year
    df['month'] = df['ener_dt'].dt.month
    df.set_index('ener_dt', inplace=True)
    df = df.asfreq('MS')

    # 결측값 확인 및 처리
    df['elec_usage'].fillna(method='ffill', inplace=True)

    # 훈련 및 테스트 데이터 분할
    train_df = df[df.index.year <= 2022]
    test_df = df[df.index.year == 2023]

    # 특성 변수와 타겟 변수 설정
    X_train = train_df[['year', 'month']]
    y_train = train_df['elec_usage']
    X_test = test_df[['year', 'month']]
    y_test = test_df['elec_usage']

    # XGBRegressor 모델 훈련
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # 예측 수행
    y_pred = model.predict(X_test)

    # 예측 값을 데이터 프레임으로 변환
    forecast_df = pd.DataFrame(y_pred, index=test_df.index, columns=['Forecast'])

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
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'Root Mean Squared Error: {rmse}')
    print(f'Mean Absolute Percentage Error: {mape}')
    print(f'R-squared: {r2}')

    # 결과 그래프 출력
    plt.figure(figsize=(12, 8))
    plt.plot(train_df.index, train_df['elec_usage'], label='Observed (Train)', color='blue')
    plt.plot(test_df.index, test_df['elec_usage'], label='Observed (Test)', color='green')
    plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red')
    plt.xlabel('Date')
    plt.ylabel('Electricity Usage')
    plt.title(f'XGBoost Forecast of Electricity Usage for {district}')
    plt.legend()
    plt.show()


# 각 구별로 모델 생성 및 평가
districts = ['대덕구', '중구', '서구', '유성구', '동구']
for district in districts:
    create_and_evaluate_model(district)
