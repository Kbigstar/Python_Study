import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import ParameterGrid
import warnings
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_engine():
    try:
        engine = create_engine('oracle+cx_oracle://?:?@0.0.0.0:1521/xe')# 1? -> user, 2? -> password, "ip:1521/xe"
        logging.info("Database connection established.")
        return engine
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise


def create_and_evaluate_model(complexcode):
    query = f"""
        SELECT ENER_DT, SUM(ELEC_USAGE) as ELEC_USAGE
        FROM TMP2
        WHERE complexcode = '{complexcode}'
        AND TO_NUMBER(TO_CHAR(TO_DATE(ENER_DT, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
        GROUP BY ENER_DT
        ORDER BY ENER_DT
    """

    try:
        engine = get_engine()
        df = pd.read_sql(query, con=engine)
        logging.info(f"Data fetched for complex code {complexcode}.")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return

    try:
        df['ener_dt'] = pd.to_datetime(df['ener_dt'], format='%Y%m')
        df.set_index('ener_dt', inplace=True)
        df = df.asfreq('MS')
        df['elec_usage'] = df['elec_usage'].ffill()
        logging.info("Data preprocessing completed.")
    except Exception as e:
        logging.error(f"Error during data preprocessing: {e}")
        return

    train_df = df[df.index.year <= 2022]
    test_df = df[df.index.year == 2023]

    exog_train = pd.DataFrame({
        'year': train_df.index.year,
        'month': train_df.index.month
    }, index=train_df.index)
    exog_test = pd.DataFrame({
        'year': test_df.index.year,
        'month': test_df.index.month
    }, index=test_df.index)

    p = d = q = range(0, 3)
    pdq = list(ParameterGrid({'p': p, 'd': d, 'q': q}))
    seasonal_pdq = [(x['p'], x['d'], x['q'], 12) for x in pdq]

    best_aic = float('inf')
    best_pdq = None
    best_seasonal_pdq = None

    warnings.filterwarnings("ignore")

    for param in pdq:
        for seasonal_param in seasonal_pdq:
            try:
                model = SARIMAX(train_df['elec_usage'], order=(param['p'], param['d'], param['q']),
                                seasonal_order=seasonal_param, exog=exog_train)
                model_fit = model.fit(disp=False)
                if model_fit.aic < best_aic:
                    best_aic = model_fit.aic
                    best_pdq = (param['p'], param['d'], param['q'])
                    best_seasonal_pdq = seasonal_param
            except:
                continue

    warnings.filterwarnings("default")

    logging.info(f"Best SARIMAX parameters: {best_pdq} x {best_seasonal_pdq} with AIC: {best_aic}")

    try:
        model = SARIMAX(train_df['elec_usage'], order=best_pdq, seasonal_order=best_seasonal_pdq, exog=exog_train)
        model_fit = model.fit(disp=False, maxiter=1000, method='nm')
        logging.info("Model fitting completed.")
    except Exception as e:
        logging.error(f"Error during model fitting: {e}")
        return

    try:
        print(model_fit.summary())
        forecast_steps = len(test_df)
        forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_test)
        forecast_values = forecast.predicted_mean
        forecast_values_only = forecast_values.values
        forecast_df = pd.DataFrame(forecast_values_only, index=test_df.index, columns=['Forecast'])
        logging.info("Forecasting completed.")
    except Exception as e:
        logging.error(f"Error during forecasting: {e}")
        return

    combined_df = test_df.copy()
    combined_df['Forecast'] = forecast_df['Forecast']
    combined_df.dropna(inplace=True)

    mse = mean_squared_error(combined_df['elec_usage'], combined_df['Forecast'])
    mae = mean_absolute_error(combined_df['elec_usage'], combined_df['Forecast'])
    rmse = np.sqrt(mse)
    r2 = r2_score(combined_df['elec_usage'], combined_df['Forecast'])

    def mean_absolute_percentage_error(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    mape = mean_absolute_percentage_error(combined_df['elec_usage'], combined_df['Forecast'])

    def mean_bias_deviation(y_true, y_pred):
        return np.mean(y_pred - y_true)

    mbd = mean_bias_deviation(combined_df['elec_usage'], combined_df['Forecast'])

    logging.info(f'Mean Squared Error: {mse}')
    logging.info(f'Mean Absolute Error: {mae}')
    logging.info(f'Root Mean Squared Error: {rmse}')
    logging.info(f'Mean Absolute Percentage Error: {mape}')
    logging.info(f'R-squared: {r2}')
    logging.info(f'Mean Bias Deviation: {mbd}')

    # 결과 시각화
    plt.figure(figsize=(10, 5))
    plt.plot(combined_df.index, combined_df['elec_usage'], label='Actual')
    plt.plot(combined_df.index, combined_df['Forecast'], label='Forecast')
    plt.legend()
    plt.title(f'Electricity Usage Forecast for Complex Code: {complexcode}')
    plt.xlabel('Date')
    plt.ylabel('Electricity Usage')
    plt.show()


# 테스트를 위해 complexcode 'A30005002' 사용
create_and_evaluate_model('A30005002')
