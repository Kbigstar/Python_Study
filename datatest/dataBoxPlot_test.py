import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# CSV 파일을 불러옵니다
file_path = 'ener.csv'
data = pd.read_csv(file_path)

# ENER_DT를 'YYYYMM' 형식의 문자열로 처리하고 datetime 형식으로 변환합니다
data['ENER_DT'] = pd.to_datetime(data['ENER_DT'].astype(str), format='%Y%m')

# 연도별 'ELEC_USAGE' 데이터 분포를 시각화합니다
data['Year'] = data['ENER_DT'].dt.year

# ELEC_USAGE의 로그 값을 추가합니다 (0 값은 제외)
data['LOG_ELEC_USAGE'] = np.log1p(data['ELEC_USAGE'])

# 연도별로 색깔을 다르게 하기 위해 색상 팔레트를 사용하여 박스플롯을 그립니다.
plt.figure(figsize=(14, 7))
sns.boxplot(x='Year', y='LOG_ELEC_USAGE', data=data, palette="Set3")
plt.title('대전광역시 전력량 이상치 분석 (2014-2023)')
plt.xlabel('Year')
plt.ylabel('LOG_ELEC_USAGE')
plt.grid(True)
plt.show()
