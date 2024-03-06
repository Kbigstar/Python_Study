# pip install opencv-python
# openCV 컴퓨터 비전의 객체 식별, 이미지 결합 및 처리에 사용
# pip install easyocr # 쉽게 OCR 기능을 사용할 수 있음.
import cv2
import matplotlib.pyplot as plt
# 이미지를 회색으로
img = cv2.imread("./img/car1.png", cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
# plt.show()
# 이미지 작게
img2 = cv2.imread('./img/car4.JPG', cv2.COLOR_BGR2RGB)
img_50 = cv2.resize(img2, (100, 100))
plt.imshow(img_50)
# plt.show()
import easyocr
# easyOCR reader 생성 (영어 한글)
reader = easyocr.Reader(['en', 'ko'], gpu=False)
test_img = cv2.imread("./img/code1.JPG")
# 이미지 텍스트 추출
results = reader.readtext(test_img)
for result in results:
    location, text, _ = result
    print(f'location:{location}, text:{text}')

