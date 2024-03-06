import matplotlib.pyplot as plt
from sklearn import datasets
import numpy as np

# 아이리스 데이터셋
iris = datasets.load_iris()
x = iris.data
y = iris.target
target_names = iris.target_names
# 꽃받침 길이와 너비
plt.figure()
markers = ['o', '^', 's']
for i, (color
 , marker) in enumerate(zip(['navy', 'turquoise','darkorange'],markers)):
    plt.scatter(x[y == i, 0], x[y == i, 1], color=color
                , marker=marker, label=target_names[i])
plt.xlabel('length')
plt.ylabel('width')
plt.legend()
# plt.show()
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# 데이터 세트
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)
pred = knn.predict(x_test)
acc = accuracy_score(y_test, pred)
print('acc:', acc)
# 테스트
sample = [[5.0, 3.6, 1.4, 0.2]]
sample_pred = knn.predict(sample)
print(iris.target_names[sample_pred][0])






