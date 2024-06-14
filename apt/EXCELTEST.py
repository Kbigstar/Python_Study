import pandas as pd

# 엑셀 파일 읽기
df = pd.read_excel('면적.xlsx')

# '시도', '시군구', '동리', '단지코드', '단지명'을 기준으로 그룹화하여 각 그룹의 '전용면적'과 '세대수'의 평균 계산
grouped_df = df.groupby(['시도', '시군구', '동리', '단지코드', '단지명']).agg({'전용면적': 'mean', '세대수': 'mean'}).reset_index()

# 새로운 엑셀 파일로 저장
grouped_df.to_excel('average_area_and_unit_count_per_apartment2.xlsx', index=False)


# 새로운 엑셀 파일로 저장
# grouped_df.to_excel('average_area_and_unit_count_per_apartment.xlsx', index=False)

# '단지코드' 열의 중복값 확인
duplicate_codes = df['단지코드'].value_counts()

# 횟수가 1보다 큰 값만 선택하여 중복된 단지코드를 출력
duplicate_codes = duplicate_codes[duplicate_codes > 1]
print("중복된 단지코드:")
print(duplicate_codes)
