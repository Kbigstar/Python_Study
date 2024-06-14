import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 파일 경로
image_path = 'bill3.jpg'

# 정답 텍스트 (예시)
ground_truth_text = """
관리비 납입영수증 (입주자용)
2024년 1월 1 동 308 호 귀하
일반 관리비 29,401 전기료 206k 29,760
청 소 비 14,461 공동 전기료 5,573
소 독 비 866 승강기전기료 1,338
승강기 유지비 3,123
수선 유지비 3,135 T V 수신료 2,500
장기수선충당금 15,889 수도료 17t 11,560
음식물 처리비 1,148 공동 수도료 225
경 비 비 26,871 공청시설유지비 4,400
화재 보험료 1,686
임대 운영비 616
위탁 관리비 613
선관위 운영비 171
관리비차감 -1,829
"""

# 이미지 로드
image = cv2.imread(image_path)

# 이미지가 올바르게 로드되었는지 확인
if image is None:
    print(f"이미지를 찾을 수 없습니다: {image_path}")
else:
    print("이미지가 성공적으로 로드되었습니다.")

    # 이미지 전처리
    # 그레이스케일 변환
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 밝기 조정
    adjusted_image = cv2.convertScaleAbs(gray_image, alpha=1.5, beta=30)

    # 어댑티브 히스토그램 평활화 (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(adjusted_image)

    # 이진화 (Thresholding)
    _, binary_image = cv2.threshold(equalized_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 노이즈 제거 (GaussianBlur)
    denoised_image = cv2.GaussianBlur(binary_image, (5, 5), 0)

    # 모폴로지 연산 (모폴로지 닫힘 연산을 사용하여 텍스트 영역 강조)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morphed_image = cv2.morphologyEx(denoised_image, cv2.MORPH_CLOSE, kernel)

    # 텍스트 영역 검출을 위한 경계 찾기
    contours, _ = cv2.findContours(morphed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 각 텍스트 영역을 개별적으로 처리
    results = []
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        roi = morphed_image[y:y+h, x:x+w]

        # 해상도 높이기
        scale_percent = 150  # 이미지 크기 비율
        width = int(roi.shape[1] * scale_percent / 100)
        height = int(roi.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(roi, dim, interpolation=cv2.INTER_LINEAR)

        # 이미지에서 텍스트 추출
        result = reader.readtext(resized_image, detail=0)
        results.extend(result)

    # 추출된 텍스트 결합
    extracted_text = " ".join(results)

    # 후처리: OCR 결과 보정 (예: 잘못 인식된 숫자/문자 보정)
    def postprocess_text(text):
        corrections = {
            'O': '0', 'I': '1', 'l': '1', 'Z': '2', 'S': '5', 'B': '8'
        }
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        return text

    processed_text = postprocess_text(extracted_text)

    # 정답 텍스트와 OCR 결과 비교
    def compare_texts(extracted, ground_truth):
        extracted_words = extracted.split()
        ground_truth_words = ground_truth.split()

        # 단어 수준에서 정확도 계산
        correct_words = 0
        for word in extracted_words:
            if word in ground_truth_words:
                correct_words += 1

        accuracy = correct_words / len(ground_truth_words) * 100
        return accuracy

    accuracy = compare_texts(processed_text, ground_truth_text)
    print(f"추출된 텍스트:\n{processed_text}\n")
    print(f"정답 텍스트:\n{ground_truth_text}\n")
    print(f"OCR 정확도: {accuracy:.2f}%")

    # 전처리된 이미지 표시 (선택 사항)
    plt.imshow(morphed_image, cmap='gray')
    plt.axis('off')
    plt.show()
