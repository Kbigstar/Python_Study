import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
# 머신러닝 라이브러리 # pip install scikit-learn

model = LinearRegression()
df = pd.read_csv("./datasets/heights.csv")
x = df['height']
y = df['weight']

sh = x.values.reshape(-1, 1)
model.fit(x.values.reshape(-1, 1), y)
print("기울기 : ", model.coef_)
print("y 절편 : ", model.intercept_)
plt.plot(x, y, 'o')
plt.plot(x, model.predict(x.values.reshape(-1, 1)))
plt.show()
print('test : ', model.predict([[70]]))