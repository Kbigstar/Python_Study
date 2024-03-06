from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
# 매번 실행할때 랜덤값이 고정될 수 있도록
np.random.seed(0)
tf.random.set_seed(0)
(x_train, y_train),(x_test, y_test) = mnist.load_data()
print(f"학습 데이터:{x_train.shape}")
print(f"테스트 데이터:{x_test.shape}")
# 데이터 준비
x_train_reshape = x_train.reshape(
    x_train.shape[0], 784).astype("float32")/255
x_test_reshape = x_test.reshape(
    x_test.shape[0], 784).astype("float32")/255
y_train_cate = to_categorical(y_train, 10)
y_test_cate = to_categorical(y_test, 10)
# model
model = Sequential()
model.add(Dense(512, input_dim=784, activation='relu'))
# softmax는 다중 클래스 분류에서 사용되는 활성화 함수
# 벡터의 원소를 0 ~ 1 사이값으로 변환 변한된 값들의 합이 1이 되도록
# 벡터를 확률 분포로 변환하는 역할을 함.
model.add(Dense(10, activation='softmax'))
model.summary()
model.compile(loss='categorical_crossentropy'
              , optimizer='adam', metrics=['acc'])
histroy = model.fit(x_train_reshape
                    ,y_train_cate
                    ,epochs=100
                    ,batch_size=200
                    ,validation_data=(x_test_reshape, y_test_cate))
v_loss = histroy.history['val_loss']
loss = histroy.history['loss']
print(f'학습 acc:{model.evaluate(x_train_reshape, y_train_cate)}')
print(f'테스트 acc:{model.evaluate(x_test_reshape, y_test_cate)}')


