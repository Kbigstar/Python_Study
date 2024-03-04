from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
model = load_model("./model/ANN.h5")
model.summary()
image = Image.open("3.png")
image = image.resize((28, 28)).convert("L") # L 흑백 28 x 28로
image = 255 - np.array(image)
plt.imshow(image, cmap='Greys')
plt.show()

x_test_sample = image.reshape(1, 784).astype("float32") / 255
pred = model.predict(x_test_sample)
print(np.argmax(pred, axis=1))

