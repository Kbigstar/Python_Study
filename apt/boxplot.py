import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

# Oracle 데이터베이스에 연결
conn = cx_Oracle.connect("?", "?", "0.0.0.0:1521/xe")

# ex_energy 테이블과 ex_apartment 테이블에서 데이터 가져오기
query = """
    SELECT e.elec_usage AS ELEC_ENERGY, e.ener_dt AS ENERGY, a.apart_buildingnm AS APART_BUILDINGNM
    FROM energy e
    JOIN apartment a ON e.complexcode = a.apart_complexcode
    WHERE e.ener_dt BETWEEN '202101' AND '202312'
    AND a.apart_complexcode = 'A10024551'
"""
df = pd.read_sql(query, con=conn)

# 전기 사용량이 0인 경우 평균값으로 대체
mean_elec_energy = df[df['ELEC_ENERGY'] != 0]['ELEC_ENERGY'].mean()
df['ELEC_ENERGY'] = df['ELEC_ENERGY'].replace(0, mean_elec_energy)

# 박스 플롯 시각화
plt.figure(figsize=(20, 10))
plt.boxplot(df['ELEC_ENERGY'])
plt.title(df['APART_BUILDINGNM'].iloc[0], fontproperties='Malgun Gothic')
plt.ylabel('Electricity Usage')
plt.xticks([1], ['Electricity Usage'])  # X축 레이블 설정
plt.tight_layout()
plt.show()

# 연결 닫기
conn.close()
