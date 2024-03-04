# pip install tensorflow==2.13
# pip install tensorflow
# pip install keras
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
(x_train, y_train),(x_test, y_test) = mnist.load_data()
print(f"학습 데이터:{x_train.shape}")
print(f"테스트 데이터:{x_test.shape}")
plt.imshow(x_train[0], cmap='Greys')
plt.show()
import sys
for x in x_train[0]:
    for i in x:
        sys.stdout.write("%d\t" %i)
    sys.stdout.write("\n")
