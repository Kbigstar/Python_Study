import pandas as pd

# 엑셀 파일 읽기
df1 = pd.read_excel('average_area_and_unit_count_per_apartment2.xlsx')
df2 = pd.read_excel('면적.xlsx')

# 각 파일의 단지코드 추출
codes_df1 = set(df1['단지코드'])
codes_df2 = set(df2['단지코드'])

# 첫 번째 파일에는 있지만 두 번째 파일에는 없는 단지코드 수 계산
codes_only_in_df1 = codes_df2 - codes_df1
num_missing_codes = len(codes_only_in_df1)

print(f"두 번째 파일에는 {num_missing_codes}개의 단지코드가 더 존재합니다.")
