import easyocr
import cv2
# pip install easyocr
# pip install opencv-python

# 이미지 읽기
image = cv2.imread('./img/car1.png')

# EasyOCR Reader 생성 (영어와 한글 지원)
reader = easyocr.Reader(['en', 'ko'])

# 이미지에서 텍스트 추출
results = reader.readtext(image)

# 결과 출력
for result in results:
    # 좌표 정보와 텍스트 정보 추출
    location, text, _ = result
    print(f'Location: {location}, Text: {text}')