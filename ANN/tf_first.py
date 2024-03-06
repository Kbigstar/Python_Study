import tensorflow as tf
import numpy as np
data = np.loadtxt("../ML/datasets/ThoraricSurgery.csv", delimiter=',')
# 독립변수 :환자의 기록 , 종속변수 : 수술후 사망0, 생존1
x = data[:, 0:17] # 모든행, 17개열
y = data[:, 17]   # 모든행, 마지막열
# 딥러닝 구조 만들기
from keras.models import Sequential
from keras.layers import Dense
model = Sequential()
# 히든 레이어 추가
model.add(Dense(30, input_dim=17, activation='relu'))
# 출력층
model.add(Dense(1, activation='sigmoid')) # 이항 분류
model.summary() #모델 구조 출력
# 손실함수와 최적화 방법 정의
model.compile(loss='mean_squared_error'
              , optimizer='adam', metrics=['acc'])
# 학습
model.fit(x, y, epochs=30, batch_size=10)
# 결과 출력
print(f'accuracy : {model.evaluate(x, y)[1]}')
