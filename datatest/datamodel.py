import itertools
import pandas as pd
from sqlalchemy import create_engine
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
import time

warnings.filterwarnings("ignore")

# SQLAlchemy 엔진 생성
engine = create_engine('oracle+cx_oracle://aner:aner@192.168.0.44:1521/xe')

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


# 최적의 파라미터 찾기 위한 Grid Search 함수
def sarima_grid_search(y, seasonal_period=12):
    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], seasonal_period) for x in pdq]
    best_aic = float("inf")
    best_params = None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = SARIMAX(y, order=param, seasonal_order=param_seasonal, enforce_stationarity=False,
                              enforce_invertibility=False)
                results = mod.fit(disp=False)
                if results.aic < best_aic:
                    best_aic = results.aic
                    best_params = (param, param_seasonal)
            except Exception as e:
                continue
    return best_params


# 예측 및 평가 함수
def predict_and_evaluate(complexcode):
    try:
        df = get_elec_usage_data(complexcode)
        df.columns = df.columns.str.lower()
        df.set_index('usage_date', inplace=True)

        train = df.iloc[:-12]
        test = df.iloc[-12:]

        # 최적의 파라미터 찾기
        best_params = sarima_grid_search(train['elec_usage'])
        if best_params is None:
            return None

        param, param_seasonal = best_params
        model = SARIMAX(train['elec_usage'], order=param, seasonal_order=param_seasonal)
        model_fit = model.fit(disp=False)

        predictions = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
        test['predicted'] = predictions

        rmse = mean_squared_error(test['elec_usage'], test['predicted'], squared=False)
        mae = mean_absolute_error(test['elec_usage'], test['predicted'])

        return {
            'complexcode': complexcode,
            'rmse': rmse,
            'mae': mae,
            'predictions': predictions.tolist()
        }
    except Exception as e:
        print(f"Error occurred for complexcode {complexcode}: {e}")
        return None


if 'complexcodes' in locals():
    print("예측 실행 중...")
    start_time = time.time()

    # 순차적으로 예측 수행
    evaluation_results = [predict_and_evaluate(code) for code in complexcodes]
    evaluation_results = [result for result in evaluation_results if result is not None]

    end_time = time.time()
    print(f"전체 예측 완료. 소요 시간: {end_time - start_time:.2f}초")

    # 리스트를 데이터프레임으로 변환
    evaluation_df = pd.DataFrame(evaluation_results)

    # 평가 결과 및 예측 출력
    print(evaluation_df)
else:
    print("Complexcodes list not defined.")
