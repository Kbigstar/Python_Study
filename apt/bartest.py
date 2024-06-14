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

# 'ENERGY' 열을 날짜 형식으로 변환하여 연도와 월을 추출
df['ENERGY'] = pd.to_datetime(df['ENERGY'], format='%Y%m')
df['YEAR'] = df['ENERGY'].dt.year
df['MONTH'] = df['ENERGY'].dt.month

# 연도별 월별 전기 사용량 계산
yearly_monthly_elec_usage = df.groupby(['YEAR', 'MONTH'])['ELEC_ENERGY'].sum().unstack()

# 데이터 프레임에서 빌딩 이름을 추출합니다. (데이터 프레임에서 첫 번째 빌딩 이름을 사용)
building_name = df['APART_BUILDINGNM'].iloc[0]

# 연도별 월별 전기 사용량 선 그래프 시각화
plt.figure(figsize=(12, 6))
for year in yearly_monthly_elec_usage.index:
    plt.plot(range(1, 13), yearly_monthly_elec_usage.loc[year], label=str(year))

# 여기에 apart_buildingnm 값을 제목에 포함시킵니다.
plt.title(f'{building_name} - 연도 월별 전력 사용량', fontproperties='Malgun Gothic')
plt.xlabel('Month')
plt.ylabel('Electricity Usage')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.grid(True)
plt.tight_layout()
plt.show()

# 연결 닫기
conn.close()

