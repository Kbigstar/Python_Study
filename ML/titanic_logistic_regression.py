import pandas as pd
df = pd.read_csv('./datasets/Titanic Passengers.csv')
print(df.columns)

# 남 : 0, 여 : 1
df['sex'] = df['sex'].map({'female': 1, 'male': 0})
print(df['sex'])

# age 널 값을 평균 값으로
df['age'].fillna(value=df['age'].mean(), inplace=True)
print(df.info())

# pclass 컬럼으로
df['first'] = df['pclass'].apply(lambda x : 1 if x == 1 else 0) # x = 1 이면 1 아니면 0 라벨링
df['business'] = df['pclass'].apply(lambda x : 1 if x == 2 else 0)
df['economy'] = df['pclass'].apply(lambda x : 1 if x == 3 else 0)
print(df.head())
print(df.columns)

x = df[['sex', 'age','first', 'business', 'economy']]
y = df[['survived']]

from sklearn.model_selection import train_test_split
# 80% 학습용 20% 테스트용
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
print(x_train.shape)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() # 스케일을 평균 0, 표준편차 1이 되도록 표준화
x_train = scaler.fit_transform(x_train) # fit_t.. 은 해당 데이터를 기준으로 표준화
x_test = scaler.transform(x_test)       # tr.. 적용된 비율로 표준화

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train, y_train)
print(model.coef_) # 기울기
print(model.intercept_) # y 절편
print("학습데이터 성능 : ", model.score(x_train, y_train))
print("테스트데이터 성능 ", model.score(x_test, y_test))

import numpy as np
Jack = np.array([0.0, 20.0, 0.0, 0.0, 1.0])
Rose = np.array([1.0, 17.0, 1.0, 0.0, 0.0])
Kbs = np.array([0.0, 26.0, 0.0, 1.0, 0.0])
Baby = np.array([1.0, 5.0, 0.0, 0.0, 1.0])
sample = np.array([Jack, Rose, Kbs, Baby])
sample = scaler.transform(sample)

# 분류
print(model.predict(sample))
# 확률
print(model.predict_proba(sample))