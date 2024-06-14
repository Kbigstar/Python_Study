import requests
import pandas as pd
import xml.etree.ElementTree as ET
from DBManager import DBManager
import time

db = DBManager()
df_apartments = pd.read_sql(con=db.conn, sql="SELECT APART_COMPLEXCODE FROM APARTMENT")
apartment_codes = df_apartments['APART_COMPLEXCODE'].tolist()

retry_delay = 1  # 재시도 대기 시간(초)
current_year = 2023  # 현재 연도 예시
current_month = 12  # 현재 월 예시

for apt_code in apartment_codes:
    if apt_code == "A30004001":  # "A30004001" 코드의 아파트는 제외 데이터가 안 넘어옴
        continue

    df_existing = pd.read_sql(con=db.conn, sql=f"SELECT MAX(ener_dt) as LAST_DATE FROM energy WHERE complexcode = '{apt_code}'")
    last_date = df_existing.iloc[0]['LAST_DATE']

    if last_date:
        last_year = int(last_date[:4])
        last_month = int(last_date[4:]) + 1
        if last_month > 12:
            last_year += 1
            last_month = 1
        # 현재 날짜보다 미래의 데이터를 요청하지 않도록 체크
        if last_year > current_year or (last_year == current_year and last_month > current_month):
            continue
    else:
        last_year = 2014
        last_month = 1

    url = 'http://apis.data.go.kr/1611000/ApHusEnergyUseInfoOfferService/getHsmpApHusUsgQtyInfoSearch'
    for year in range(last_year, 2024):
        start_month = last_month if year == last_year else 1
        for month in range(start_month, 13):
            # 현재 날짜 이후의 데이터 요청 방지
            if year > current_year or (year == current_year and month > current_month):
                break
            reqDate = f"{year}{month:02d}"
            print(apt_code)
            print(reqDate)
            params = {
                'serviceKey': 'U2YtjnVOpuUnQot+3JDMqOONPmmJA7Lg+Bj1qr7JbjHjNi7lCHXo9H8IzyDYRYFYr6C/K0fDYL24sjyet3OYfA==',
                'kaptCode': apt_code,
                'reqDate': reqDate
            }
            response_successful = False
            while not response_successful:
                try:
                    response = requests.get(url, params=params, timeout=10)
                    print(response.text)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        if root.find('.//errmsg') is None:
                            response_successful = True
                            data = {
                                'complexcode': apt_code,
                                'ener_dt': reqDate,
                                'heat_amount': root.find('.//heat').text,
                                'heat_usage': root.find('.//hheat').text,
                                'waterhot_amount': root.find('.//waterHot').text,
                                'waterhot_usage': root.find('.//hwaterHot').text,
                                'gas_amount': root.find('.//gas').text,
                                'gas_usage': root.find('.//hgas').text,
                                'elec_amount': root.find('.//elect').text,
                                'elec_usage': root.find('.//helect').text,
                                'water_amount': root.find('.//waterCool').text,
                                'water_usage': root.find('.//hwaterCool').text
                            }
                            db.insert("""
                                INSERT INTO energy (complexcode, ener_dt, heat_amount, heat_usage, waterhot_amount, waterhot_usage, gas_amount, gas_usage, elec_amount, elec_usage, water_amount, water_usage)
                                VALUES (:complexcode, :ener_dt, :heat_amount, :heat_usage, :waterhot_amount, :waterhot_usage, :gas_amount, :gas_usage, :elec_amount, :elec_usage, :water_amount, :water_usage)
                                """, data)
                            time.sleep(retry_delay)
                        else:
                            errmsg = root.find('.//errmsg').text
                            print(f"API Error: {errmsg} - Retrying after {retry_delay} seconds...")
                            time.sleep(retry_delay)
                    else:
                        print(f"HTTP Error: Status code {response.status_code} - Retrying...")
                        time.sleep(retry_delay)
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e} - Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)
