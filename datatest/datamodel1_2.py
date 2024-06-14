import itertools
import pandas as pd
from sqlalchemy import create_engine
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from concurrent.futures import ProcessPoolExecutor
import warnings

warnings.filterwarnings("ignore")

def get_engine():
    return create_engine('oracle+cx_oracle://aner:aner@192.168.0.44:1521/xe')

def get_complexcodes(engine):
    query_complexcode_no_zero = """
    SELECT COMPLEXCODE
    FROM TMP2
    WHERE TO_NUMBER(TO_CHAR(TO_DATE(ENER_DT, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
    GROUP BY COMPLEXCODE
    HAVING COUNT(CASE WHEN ELEC_USAGE = 0 THEN 1 ELSE NULL END) = 0
    """
    df_complexcode_no_zero = pd.read_sql(query_complexcode_no_zero, con=engine)
    df_complexcode_no_zero.columns = [col.lower() for col in df_complexcode_no_zero.columns]
    return df_complexcode_no_zero['complexcode'].tolist()

def get_elec_usage_data(engine, complexcode):
    query = f"""
    SELECT TO_DATE(ENER_DT, 'YYYYMM') AS usage_date, ELEC_USAGE
    FROM TMP2
    WHERE COMPLEXCODE = '{complexcode}'
    AND TO_DATE(ENER_DT, 'YYYYMM') BETWEEN TO_DATE('201401', 'YYYYMM') AND TO_DATE('202312', 'YYYYMM')
    ORDER BY TO_DATE(ENER_DT, 'YYYYMM')
    """
    result = pd.read_sql(query, con=engine)
    result['usage_date'] = pd.to_datetime(result['usage_date'])
    result.set_index('usage_date', inplace=True)
    result = result.asfreq('MS')  # 명시적으로 빈도를 설정
    return result

def sarima_grid_search(y, seasonal_period=12):
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], seasonal_period) for x in pdq]
    best_aic = float("inf")
    best_params = None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = SARIMAX(y, order=param, seasonal_order=param_seasonal, enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit(disp=False)
                if results.aic < best_aic:
                    best_aic = results.aic
                    best_params = (param, param_seasonal)
            except Exception:
                continue
    return best_params

def predict_and_evaluate(complexcode):
    try:
        engine = get_engine()
        df = get_elec_usage_data(engine, complexcode)
        df.columns = df.columns.str.lower()

        train = df.iloc[:-12]
        test = df.iloc[-12:]

        best_params = sarima_grid_search(train['elec_usage'])
        if best_params is None:
            return None

        param, param_seasonal = best_params
        model = SARIMAX(train['elec_usage'], order=param, seasonal_order=param_seasonal)
        model_fit = model.fit(disp=False)

        predictions = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
        test.loc[:, 'predicted'] = predictions

        rmse = mean_squared_error(test['elec_usage'], test['predicted'], squared=False)
        mae = mean_absolute_error(test['elec_usage'], test['predicted'])

        return {
            'complexcode': complexcode,
            'rmse': rmse,
            'mae': mae,
            'predictions': test['predicted'].tolist()
        }
    except Exception as e:
        print(f"Error occurred for complexcode {complexcode}: {e}")
        return None

if __name__ == '__main__':
    print("예측 실행 중...")
    engine = get_engine()
    complexcodes = get_complexcodes(engine)

    with ProcessPoolExecutor() as executor:
        evaluation_results = list(executor.map(predict_and_evaluate, complexcodes))

    evaluation_results = [result for result in evaluation_results if result is not None]
    evaluation_df = pd.DataFrame(evaluation_results)

    print(evaluation_df)
