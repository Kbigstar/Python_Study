from keras.applications import vgg16
from keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

# 학습 되어있는 모델 가져오기
model = vgg16.VGG16()
model.summary()
def fn_predict(p_model, p_file):
     image = load_img(p_file, target_size=(224, 224))
     plt.imshow(image)
     plt.show()
     # 학습된 모델의 input shape으로
     test_image = img_to_array(image).reshape((1, 224, 224, 3))
     test_image = vgg16.preprocess_input(test_image)
     pred = p_model.predict(test_image)
     label = vgg16.decode_predictions(pred)
     pred_cls = label[0][0]
     print(pred_cls[1], pred_cls[2]*100)
import os
path = './imageNet/'
for f in os.listdir(path):
    fn_predict(model, path + f)