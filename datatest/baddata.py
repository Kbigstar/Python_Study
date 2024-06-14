import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows에서 'Malgun Gothic' 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# CSV 파일을 불러옵니다
file_path = 'ener.csv'
data = pd.read_csv(file_path)

# 'ENER_DT'를 datetime 형식으로 변환합니다
data['ENER_DT'] = pd.to_datetime(data['ENER_DT'].astype(str), format='%Y%m')

# A30017005 단지코드의 데이터만 선택합니다
data_A30017005 = data[(data['COMPLEXCODE'] == 'A30017005') & (data['ENER_DT'].dt.year == 2017)]

# 2017년 1월부터 12월까지의 데이터만 선택합니다
data_A30017005_2017 = data_A30017005[(data_A30017005['ENER_DT'].dt.month >= 1) & (data_A30017005['ENER_DT'].dt.month <= 12)]

# 'ENER_DT'별로 'ELEC_USAGE'를 시각화합니다
plt.figure(figsize=(12, 6))
plt.bar(data_A30017005_2017['ENER_DT'].dt.strftime('%Y-%m'), data_A30017005_2017['ELEC_USAGE'], color='skyblue', width=0.6)

# 그래프의 제목과 축 레이블을 설정합니다
plt.title('대전삼성1 전력량')
plt.xlabel('Date')
plt.ylabel('ELEC_USAGE (kWh)')
plt.xticks(rotation=45)

# X축에 매월이 찍히게 설정합니다
plt.gca().set_xticks(data_A30017005_2017['ENER_DT'].dt.strftime('%Y-%m'))

plt.tight_layout()

# 그래프를 표시합니다
plt.show()

# 월별 ELEC_USAGE 출력
print("2017년 월별 ELEC_USAGE:")
for idx, row in data_A30017005_2017.iterrows():
    print(f"{row['ENER_DT'].strftime('%Y-%m')}: {row['ELEC_USAGE']} kWh")
