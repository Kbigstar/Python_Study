import pandas as pd
from DBManager import DBManager
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows의 경우)
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# DB 연결
db = DBManager()

# 각 구별 2023년 월별 전력 사용량을 조회하는 쿼리
query_monthly_usage_2023 = """
SELECT a.APART_DISTRICT AS district, SUBSTR(t.ener_dt, 5, 2) AS month, SUM(t.elec_usage) AS total_elec_usage
FROM tmp2 t
JOIN apartment a ON t.COMPLEXCODE = a.APART_COMPLEXCODE
WHERE a.APART_DISTRICT IN ('유성구', '서구', '중구', '대덕구', '동구')
  AND SUBSTR(t.ener_dt, 1, 4) = '2023'
GROUP BY a.APART_DISTRICT, SUBSTR(t.ener_dt, 5, 2)
ORDER BY a.APART_DISTRICT, SUBSTR(t.ener_dt, 5, 2)
"""

df_monthly_usage_2023 = pd.read_sql(query_monthly_usage_2023, con=db.conn)

# 데이터프레임 컬럼명 확인
print(df_monthly_usage_2023.columns)

# 색상 설정
colors = {
    '대덕구': 'lightcoral',  # 연한 빨간색
    '동구': 'orange',       # 색깔 그대로
    '서구': 'blue',         # 짙은 파란색
    '유성구': 'plum',        # 연보라색
    '중구': 'green'          # 초록색
}

# 각 구별로 2023년 월별 전력 사용량 선 그래프 그리기
fig, ax = plt.subplots(figsize=(15, 10))

for district in df_monthly_usage_2023['DISTRICT'].unique():
    district_data = df_monthly_usage_2023[df_monthly_usage_2023['DISTRICT'] == district]
    ax.plot(district_data['MONTH'], district_data['TOTAL_ELEC_USAGE'], marker='o', label=district, color=colors[district])

# 축 및 레이블 설정
ax.set_title('구별 2023년 월별 아파트 전력 사용량', fontsize=15)
ax.set_xlabel('월', fontsize=12)
ax.set_ylabel('총 전력 사용량 (단위: 1억 kWh)', fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(range(1, 13))
ax.grid(axis='y')

# 범례를 오른쪽에 배치하고 크기 키우기
ax.legend(title='구', loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})

plt.tight_layout()

# 그래프 저장 (현재 작업 디렉토리로 경로 변경)
plt.savefig('monthly_electricity_usage_by_district_2023.png')

# 그래프 출력
plt.show()

db.conn.close()
