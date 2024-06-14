import requests
from DBManager import DBManager
import pandas as pd
import xml.etree.ElementTree as ET

# DB에서 단지 코드 리스트 가져오기
db = DBManager()
df_apartments = pd.read_sql(con=db.conn,
                            sql="SELECT DISTINCT APRAT_COMPLEXCODE FROM ex_apartment WHERE apart_district = '서구'")
apartment_codes = df_apartments['APRAT_COMPLEXCODE'].tolist()

# reqDate를 201401부터 202312까지 반복하여 API 요청 보내기
for apt_code in apartment_codes:
    url = 'http://apis.data.go.kr/1611000/ApHusEnergyUseInfoOfferService/getHsmpApHusUsgQtyInfoSearch'
    for year in range(2014, 2024):  # 2014부터 2023까지
        for month in range(1, 13):  # 1월부터 12월까지
            reqDate = f"{year}{month:02d}"  # 연도와 월을 합쳐서 reqDate 형식으로 만듦
            params = {
                'serviceKey': 'U2YtjnVOpuUnQot+3JDMqOONPmmJA7Lg+Bj1qr7JbjHjNi7lCHXo9H8IzyDYRYFYr6C/K0fDYL24sjyet3OYfA==',
                'kaptCode': apt_code,
                'reqDate': reqDate
            }
            response = requests.get(url, params=params)

            # XML 데이터 파싱
            root = ET.fromstring(response.content)
            elec_energy = root.find('.//helect').text
            water_energy = root.find('.//hwaterCool').text

            # ex_energy 테이블에 삽입
            query = "INSERT INTO ex_energy (complexcode, energy, elec_energy, water_energy) VALUES (:1, :2, :3, :4)"
            param = (apt_code, reqDate, elec_energy, water_energy)
            db.insert(query, param)
