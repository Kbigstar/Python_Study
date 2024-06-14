import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings

warnings.filterwarnings("ignore")

# SQLAlchemy 엔진 생성
engine = create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe') # 1? -> user, 2? -> password, "ip:1521/xe"

# elec_usage가 0인 레코드가 하나도 없는 complexcode 조회
query_complexcode_no_zero = """
SELECT COMPLEXCODE
FROM TMP2
WHERE TO_NUMBER(TO_CHAR(TO_DATE(ENER_DT, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
GROUP BY COMPLEXCODE
HAVING COUNT(CASE WHEN ELEC_USAGE = 0 THEN 1 ELSE NULL END) = 0
"""
df_complexcode_no_zero = pd.read_sql(query_complexcode_no_zero, con=engine)
df_complexcode_no_zero.columns = [col.lower() for col in df_complexcode_no_zero.columns]
complexcodes = df_complexcode_no_zero['complexcode'].tolist()

# 각 complexcode의 전력 사용량 데이터를 가져오는 함수
def get_elec_usage_data(complexcode):
    query = f"""
    SELECT TO_DATE(ENER_DT, 'YYYYMM') AS usage_date, ELEC_USAGE
    FROM TMP2
    WHERE COMPLEXCODE = '{complexcode}'
    AND TO_DATE(ENER_DT, 'YYYYMM') BETWEEN TO_DATE('201401', 'YYYYMM') AND TO_DATE('202312', 'YYYYMM')
    ORDER BY TO_DATE(ENER_DT, 'YYYYMM')
    """
    result = pd.read_sql(query, con=engine)
    result['usage_date'] = pd.to_datetime(result['usage_date'])
    return result

# 예측을 위한 함수
def predict_for_complexcode(code):
    try:
        df = get_elec_usage_data(code)
        df.columns = df.columns.str.lower()
        df.set_index('usage_date', inplace=True)
        df = df.asfreq('M').fillna(0)  # 월별 빈도를 설정하고 결측값을 0으로 채움

        # Prophet 모델을 위한 데이터 형식 변환
        df.reset_index(inplace=True)
        df.rename(columns={'usage_date': 'ds', 'elec_usage': 'y'}, inplace=True)

        # Prophet 모델 정의 및 훈련
        model = Prophet()
        model.fit(df)

        # 202401 예측
        future = model.make_future_dataframe(periods=1, freq='M')
        forecast = model.predict(future)
        predicted_mean = forecast.loc[forecast['ds'] == '2024-01-31', 'yhat'].values[0]

        return {'complexcode': code, 'date': '2024-01', 'predicted_elec_usage': predicted_mean}
    except Exception as e:
        print(f"Error occurred for complexcode {code}: {e}")
        return None

if 'complexcodes' in locals():
    # 순차적으로 예측 수행
    predictions_list = [predict_for_complexcode(code) for code in complexcodes]
    predictions_list = [pred for pred in predictions_list if pred is not None]

    # 리스트를 데이터프레임으로 변환
    predictions = pd.DataFrame(predictions_list)

    # 예측 결과 출력
    print(predictions)
else:
    print("Complexcodes list not defined.")
