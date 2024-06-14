import pandas as pd
from DBManager import DBManager

# DB 연결
db = DBManager()

# A30022003의 elec_usage가 500000을 넘는 데이터를 조회
query_usage = """
SELECT COMPLEXCODE, ENER_DT, ELEC_USAGE
FROM TMP2
WHERE COMPLEXCODE = 'A10025040'
  AND ELEC_USAGE > 500000
  AND TO_NUMBER(SUBSTR(ENER_DT, 1, 6)) BETWEEN 201401 AND 202312
"""

df_usage = pd.read_sql(query_usage, con=db.conn)

# 조회된 데이터가 있는지 확인
if df_usage.empty:
    print("조회된 데이터가 없습니다.")
else:
    # 평균값으로 대체할 새로운 값을 저장할 리스트
    updated_values = []

    for idx, row in df_usage.iterrows():
        complexcode = row['COMPLEXCODE']
        ener_dt = row['ENER_DT']
        elec_usage = row['ELEC_USAGE']
        year = ener_dt[:4]
        month = ener_dt[4:6]

        if month in ['07', '08']:
            # 다른 연도의 동일 월의 평균값 계산
            query_avg = f"""
            SELECT ROUND(AVG(ELEC_USAGE)) as AVG_USAGE
            FROM TMP2
            WHERE COMPLEXCODE = '{complexcode}'
              AND SUBSTR(ENER_DT, 5, 2) = '{month}'
              AND ENER_DT != '{ener_dt}'
              AND ELEC_USAGE <= 500000
            """
        else:
            # 7월과 8월을 제외한 해당 연도의 평균값 계산
            query_avg = f"""
            SELECT ROUND(AVG(ELEC_USAGE)) as AVG_USAGE
            FROM TMP2
            WHERE COMPLEXCODE = '{complexcode}'
              AND SUBSTR(ENER_DT, 1, 4) = '{year}'
              AND SUBSTR(ENER_DT, 5, 2) NOT IN ('07', '08')
              AND ENER_DT != '{ener_dt}'
              AND ELEC_USAGE <= 500000
            """

        df_avg = pd.read_sql(query_avg, con=db.conn)
        avg_usage = df_avg['AVG_USAGE'].iloc[0]

        if not pd.isna(avg_usage) and avg_usage != elec_usage:
            updated_values.append((complexcode, ener_dt, elec_usage, avg_usage))

    # 변경된 값 출력 및 업데이트
    cursor = db.conn.cursor()
    if updated_values:
        for value in updated_values:
            complexcode, ener_dt, elec_usage, avg_usage = value
            print(
                f"COMPLEXCODE: {complexcode}, ENER_DT: {ener_dt}, ORIGINAL_ELEC_USAGE: {elec_usage}, UPDATED_ELEC_USAGE: {avg_usage}")

            # 업데이트 쿼리 실행
            update_query = f"""
            UPDATE TMP2
            SET ELEC_USAGE = {avg_usage}
            WHERE COMPLEXCODE = '{complexcode}' AND ENER_DT = '{ener_dt}'
            """
            cursor.execute(update_query)
        db.conn.commit()  # 변경 사항을 커밋
    else:
        print("변경된 값이 없습니다.")

    cursor.close()

db.conn.close()
