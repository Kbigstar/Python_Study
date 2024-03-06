import numpy as np
# 퍼셉트론의 활성함수 step function
def step_function(sum):
    if sum > 0:
        return 1
    return 0
class Perceptron:
    def __init__(self, input_size):
        self.w = np.zeros(input_size + 1) # +1bias
    def predict(self, inputs):
        sum = np.dot(inputs, self.w[1:]) + self.w[0]
        return step_function(sum)

    def train(self, train_inputs, labels, lr=0.01, epochs=100):
        for i in range(epochs):
            for input, label in zip(train_inputs, labels):
                pred = self.predict(input)
                self.w[1:] += lr * (label - pred) * input
                self.w[0]  +=lr * (label - pred)
# 연산 데이터
x = np.array([[0, 0],[0, 1],[1, 0],[1, 1]])
# y = np.array([0, 1, 1, 1]) # or 연산 정답
# y = np.array([0, 0, 0, 1])   # and 연산 정답
y = np.array([0, 1, 1, 0])   # xor 연산 정답
model = Perceptron(2)
model.train(x, y, lr=0.1)
for i, v in zip(x, y):
    pred = model.predict(i)
    print(f"입력:{i}, 예측:{pred}, 실제:{v}")

# 신경망
from sklearn.neural_network import MLPClassifier
m_model = MLPClassifier(hidden_layer_sizes=(4,), activation='relu'
                      ,max_iter=10000, random_state=1)
m_model.fit(x, y)
print(m_model.predict(x))