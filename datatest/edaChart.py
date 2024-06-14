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

# 각 구별 연도별 전력 사용량을 조회하는 쿼리
query_district_yearly_usage = """
SELECT a.APART_DISTRICT AS district, SUBSTR(t.ener_dt, 1, 4) AS year, SUM(t.elec_usage) AS total_elec_usage
FROM tmp2 t
JOIN apartment a ON t.COMPLEXCODE = a.APART_COMPLEXCODE
WHERE a.APART_DISTRICT IN ('유성구', '서구', '중구', '대덕구', '동구')
  AND SUBSTR(t.ener_dt, 1, 4) >= '2018'
GROUP BY a.APART_DISTRICT, SUBSTR(t.ener_dt, 1, 4)
ORDER BY SUBSTR(t.ener_dt, 1, 4), a.APART_DISTRICT
"""

df_district_yearly_usage = pd.read_sql(query_district_yearly_usage, con=db.conn)

# 데이터프레임 컬럼명 확인
print(df_district_yearly_usage.columns)

# 각 연도별로 5개의 막대 그래프를 그리기 위해 데이터 변환
years = df_district_yearly_usage['YEAR'].unique()
districts = df_district_yearly_usage['DISTRICT'].unique()

# 연도별로 그룹화하여 데이터 준비
data_by_year = df_district_yearly_usage.pivot(index='YEAR', columns='DISTRICT', values='TOTAL_ELEC_USAGE')

# 색상 설정
colors = {
    '대덕구': 'lightcoral',  # 연한 빨간색
    '동구': 'orange',       # 색깔 그대로
    '서구': 'blue',         # 짙은 파란색
    '유성구': 'plum',        # 연보라색
    '중구': 'green'          # 초록색
}

# 막대 그래프 그리기
fig, ax = plt.subplots(figsize=(15, 10))

# 막대의 폭 및 위치 설정
bar_width = 0.15
bar_positions = list(range(len(years)))
for i, district in enumerate(districts):
    ax.bar([p + bar_width*i for p in bar_positions], data_by_year[district], bar_width, label=district, color=colors[district])

# 축 및 레이블 설정
ax.set_title('연도별 시군구별 아파트 전력 사용량', fontsize=15)
ax.set_xlabel('연도', fontsize=12)
ax.set_ylabel('총 전력 사용량 (단위: 1억 kWh)', fontsize=12)
ax.set_xticks([p + bar_width*2 for p in bar_positions])
ax.set_xticklabels(years, rotation=45)
ax.grid(axis='y')

# Y축 눈금 조정
yticks = [0, 1e8, 2e8, 3e8, 4e8]  # Y축 눈금 설정
ytick_labels = ['0', '1', '2', '3', '4']  # 눈금 라벨 설정
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels)

# 범례를 오른쪽에 배치하고 크기 키우기
ax.legend(title='구', loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12})

plt.tight_layout()

# 그래프 저장 (현재 작업 디렉토리로 경로 변경)
plt.savefig('yearly_electricity_usage_by_district_from_2018.png')

# 그래프 출력
plt.show()
