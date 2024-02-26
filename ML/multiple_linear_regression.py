# 다중 선형 회귀
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv("./datasets/streeteasy/manhattan.csv")
print(df.describe())
print(df.columns)
print(df.info())

x = df[['bedrooms', 'bathrooms', 'size_sqft',
       'min_to_subway', 'floor', 'building_age_yrs', 'no_fee', 'has_roofdeck',
       'has_washer_dryer', 'has_doorman', 'has_elevator', 'has_dishwasher',
       'has_patio', 'has_gym']]
y = df[['rent']]

# 학습 데이터 80%, 테스트 20%로 분할
# random_state = 1 설정시 다음 실행에도 동일하게 분류해줌
# 미 설정시 매번 다르게 분류해줌
# 항상 다음 실행시 동일한 인덱스의 대상건으로 선택되게 하려면 random_state = 정수
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)

model = LinearRegression()
model.fit(x_train, y_train)
print("기울기 : ", model.coef_)
print("y절편 : ", model.intercept_)
print("모델 정확도")
print("테스트 데이터 정확도 : ", model.score(x_test, y_test))
print("학습 데이터 정확도 : ", model.score(x_train, y_train))

y_hat = model.predict(x_test)
import matplotlib.pyplot as plt
plt.scatter(y_test, y_hat, alpha=0.4)
plt.xlabel('actual rent')
plt.ylabel('predict rent')
plt.show()


test_row = x_test.iloc[[1]] # 1번째 행
actual = y_test.iloc[[1]]

print("test 1행 ", test_row)
print("테스트 실제값 ",actual['rent'].values)
pre = model.predict(test_row)
print("테스트 예측값 ", pre[0])