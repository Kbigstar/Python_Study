import pandas as pd

# CSV 파일 경로 설정
file_path = 'ener.csv'

# CSV 파일을 불러옵니다
data = pd.read_csv(file_path)

# ELEC_USAGE 열의 기본 통계 정보를 요약합니다
elec_usage_description = data['ELEC_USAGE'].describe()

# 통계 정보를 정수형으로 반올림하여 출력합니다
elec_usage_description = elec_usage_description.round().astype(int)

# 통계 정보를 출력합니다
print("ELEC_USAGE describe")
print(elec_usage_description)
