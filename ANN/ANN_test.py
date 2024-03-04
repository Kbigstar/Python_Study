from keras.models import load_model
from keras.datasets import mnist

model = load_model("./model/ANN.h5")
model.summary()

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test_sample = x_test[2].reshape(1, 784).astype("float32") / 255
pred = model.predict(x_test_sample)

import matplotlib.pyplot as plt
import numpy as np
plt.imshow(x_test[2], cmap='Greys')
plt.show()
print(np.argmax(pred, axis=1))