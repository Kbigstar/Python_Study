import pandas as pd
# 판다스는 보통 별칭을 pd 로 사용
# 데이터 프레임을 자료구조로 사용 (행, 열)

dic = {"name" : ["nick", "judy", "alex"]
       , "age" : [10, 15, 20]}
# python의 딕셔너리를 쉽게 데이터 프레임으로 만들 수 있음.
df = pd.DataFrame(dic)
# 데이터 정보 출력
print(df.head())

# 기존 열을 활용하여 새로운 열을 쉽게 만들 수 있음.
df['age_plus'] = df['age'] + 1
df['age_squared'] = df['age'] * df['age']
print(df.head())

# 다양한 내장함수가 있ㅇ므.
print("총합 : ", df['age'].sum())
print("중앙값 : ", df['age'].quantile(0.5))
print("기초 통계")
print(df.describe())
print("기본 정보")
print(df.info())

# join 가능
df2 = pd.DataFrame({"name" : ["nick", "judy", "alex"]
                    ,"height" : [180, 165, 175]
                    , "gender" : ["M", "F", "M"]})
joined = df.set_index("name").join(df2.set_index("name"))
print(joined.head())

# group by 기능
g_df = joined.groupby("gender").mean()
print(g_df)

