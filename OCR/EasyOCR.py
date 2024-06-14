import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

# 이미지 파일 경로
image_path = 'bill4.jpg'

# EasyOCR 리더 초기화
reader = easyocr.Reader(['ko', 'en'], gpu=False)

REQUIRED_WORDS = ['허용된단어1', '허용된단어2']  # 허용할 단어 목록

# 이미지 로드
image = cv2.imread(image_path)

# 이미지가 올바르게 로드되었는지 확인
if image is None:
    print(f"이미지를 찾을 수 없습니다: {image_path}")
else:
    print("이미지가 성공적으로 로드되었습니다.")

    # 이미지 전처리
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이미지에서 텍스트 추출 (상세 정보 포함)
    results = reader.readtext(gray_image, detail=1)

    # 추출된 텍스트 결합
    extracted_text = " ".join([result[1] for result in results])


    # 후처리: OCR 결과 보정 (예: 잘못 인식된 숫자/문자 보정)
    def postprocess_text(text):
        corrections = {
            'O': '0', 'I': '1', 'l': '1', 'Z': '2', 'S': '5', 'B': '8'
        }
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        return text


    processed_text = postprocess_text(extracted_text)

    # OCR 결과 출력 (디버깅용)
    print(f"추출된 텍스트:\n{processed_text}\n")

    # 허용된 단어가 포함되어 있는지 확인
    word_found = any(re.search(word, processed_text, re.IGNORECASE) for word in REQUIRED_WORDS)

    if word_found:
        # 숫자와 'k'를 포함한 텍스트 필터링
        filtered_texts = [result[1] for result in results if re.search(r'\d+k', result[1], re.IGNORECASE)]

        if filtered_texts:
            print("숫자와 'k'를 포함한 텍스트 추출 성공:")
            for text in filtered_texts:
                print(text)
        else:
            print("숫자와 'k'를 포함하는 텍스트를 찾을 수 없습니다.")
    else:
        print("추출된 텍스트에 허용된 단어가 포함되어 있지 않습니다.")

    # 전처리된 이미지 표시 (선택 사항)
    plt.imshow(gray_image, cmap='gray')
    plt.axis('off')
    plt.show()
