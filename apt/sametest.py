# '단지코드' 열의 중복값 확인
duplicate_codes = grouped_df['단지코드'].value_counts()

# 횟수가 1보다 큰 값만 선택하여 중복된 단지코드를 출력
duplicate_codes = duplicate_codes[duplicate_codes > 1]
print("중복된 단지코드:")
print(duplicate_codes)
