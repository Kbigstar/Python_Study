from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용


# 데이터베이스 연결 함수
def get_engine():
    return create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe')


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
    household_query = f"""
        SELECT SUM(SIZE_HOUSEHOLDSNO) AS TOTAL_HOUSEHOLDS
        FROM APT_SIZE
        WHERE APART_COMPLEXCODE = '{complexcode}'
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
    train_df = df[df.index.year <= 2023]
    test_df = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')

    # 외생 변수 준비
    exog_train = pd.DataFrame({
        'year': train_df.index.year,
        'month': train_df.index.month
    }, index=train_df.index)
    exog_test = pd.DataFrame({
        'year': test_df.year,
        'month': test_df.month
    }, index=test_df)

    # SARIMAX 모델 적합
    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)
    model = SARIMAX(train_df['elec_usage'], order=order, seasonal_order=seasonal_order, exog=exog_train)
    model_fit = model.fit(disp=False)

    # 예측 수행
    forecast_steps = len(test_df)
    forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_test)
    forecast_values = forecast.predicted_mean

    # 예측값을 반올림하여 정수로 변환
    forecast_values_only = np.round(forecast_values.values).astype(int)

    # 총 가구수 계산
    household_df = pd.read_sql(household_query, con=engine)
    print(household_df)  # 가구 수 데이터 프레임 출력
    total_households = int(household_df['total_households'].iloc[0])

    # 예측값을 총 가구수로 나누고 정수로 반올림하여 반환
    forecast_values_per_household = np.round(forecast_values_only / total_households).astype(int)
    forecast_df = pd.DataFrame(forecast_values_per_household, index=test_df, columns=['Forecast'])

    # 요금 조회 및 추가
    forecast_with_bill = []
    for date, value in forecast_df['Forecast'].items():
        month = date.month
        if month in [7, 8]:
            bill_query = f"""
                SELECT TOTAL_BILL_AMOUNT
                FROM ELEC_SUMMER
                WHERE ELEC_USEAGE = {value}
            """
        else:
            bill_query = f"""
                SELECT TOTAL_BILL_AMOUNT
                FROM ELEC_OTHER
                WHERE ELEC_USEAGE = {value}
            """

        bill_df = pd.read_sql(bill_query, con=engine)
        if not bill_df.empty:
            total_bill_amount = int(bill_df['total_bill_amount'].iloc[0])
        else:
            total_bill_amount = None

        forecast_with_bill.append({
            'date': date.strftime('%Y-%m-%d'),
            'forecast': int(value),
            'total_bill_amount': total_bill_amount
        })

    # 결과 반환
    return forecast_with_bill


# JSON 데이터 반환을 위한 Flask 엔드포인트
@app.route('/codeForecast', methods=['POST'])
def get_forecast():
    data = request.get_json()
    complexcode = data.get('complexcode')  # 'complexcode' 값이 없으면 None이 반환됨
    results = create_and_evaluate_model(complexcode)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5556)
