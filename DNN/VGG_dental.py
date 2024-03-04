from keras import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator

train_dir = './dental_image/train'
test_dir = '/dental_image/test'

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