import pandas as pd

# 데이터 로드
df = pd.read_csv('ener.csv')

# 데이터 요약 통계 출력
summary = df.describe(include='all')
print(summary)
