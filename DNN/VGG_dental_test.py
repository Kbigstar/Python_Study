from keras import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator

train_dir = './dental_image/train'
test_dir = './dental_image/test'

# 이미지 증강(학습 데이터가 너무 적을때)
train_gen = ImageDataGenerator(
     rotation_range=180 # 180도 회전
    ,width_shift_range=0.2 # 좌우 이동
    ,height_shift_range=0.2 # 상하 이동
    ,horizontal_flip=True # 상하 이동
    ,vertical_flip=True # 상하 반적
    ,brightness_range=[0.5, 1.5] # 명암 증강
)

test_gen = ImageDataGenerator()
train_generator = train_gen.flow_from_directory(train_dir
                                                , target_size=(224, 224), batch_size=32
                                                , class_mode='categorical', shuffle=True)

test_generator = test_gen.flow_from_directory(test_dir
                                                , target_size=(224, 224), batch_size=32
                                                , class_mode='categorical', shuffle=True)

# 분류 클래스 수
class_num = len(train_generator.class_indices)
# 클래스의 명칭
labels = list(train_generator.class_indices.keys())

from keras.models import load_model
from keras.utils import load_img, img_to_array
import matplotlib.pyplot as plt
import numpy as np

model = load_model('dental_model.h5')
model.summary()


def fn_predict(p_model, p_file):
    image = load_img(p_file, target_size=(224, 224))
    plt.imshow(image)
    plt.show()
    # 학습된 모델의 input shape으로
    test_image = img_to_array(image).reshape((1, 224, 224, 3))
    pred = p_model.predict(test_image)
    idx = np.argmax(pred)
    pred_cls = labels[idx]
    print(pred_cls, pred[0][idx] * 100)

import os
path = './dental_image/test/cured/'
for f in os.listdir(path):
    fn_predict(model, path + f)