import pandas as pd
from DBManager import DBManager

def delete_records(db, codes):
    query_delete = "DELETE FROM tmp2 WHERE complexcode = :code"
    for code in codes:
        db.insert(query_delete, {'code': code})  # insert 메소드를 재사용하여 DELETE 쿼리 실행
    print(f"Deleted entries for complexcodes: {codes}")

db = DBManager()
# 삭제할 complexcode 조회
query_select = """
SELECT complexcode
FROM tmp2
WHERE TO_NUMBER(TO_CHAR(TO_DATE(ener_dt, 'YYYYMM'), 'YYYYMM')) BETWEEN 201401 AND 202312
GROUP BY complexcode
HAVING COUNT(*) = COUNT(CASE WHEN elec_usage = 0 THEN 1 ELSE NULL END)
       AND COUNT(*) = (2023 - 2014 + 1) * 12
"""
df_delete_codes = pd.read_sql(query_select, con=db.conn)

# 조회된 complexcode들을 리스트로 변환
delete_codes = df_delete_codes['COMPLEXCODE'].tolist()

# 삭제 쿼리 실행
delete_records(db, delete_codes)
