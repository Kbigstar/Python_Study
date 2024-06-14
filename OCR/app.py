from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용합니다

# EasyOCR 리더 초기화
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 허용된 파일 확장자 목록
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 허용된 단어 목록
ALLOWED_WORDS = ['관리비', '납입영수증', '(입주자용)', '전기료']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/billUpload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Read the image file
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

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

        # 허용된 단어만 필터링
        allowed_texts = [word for word in ALLOWED_WORDS if word in processed_text]

        if len(allowed_texts) < 2:
            return jsonify({"error": "Not enough allowed words found in the image"}), 400

        # 숫자와 'k'를 포함한 텍스트 필터링 및 후처리
        filtered_texts = [postprocess_text(result[1]) for result in results if re.search(r'\d+k', result[1], re.IGNORECASE)]
        filtered_numbers = [int(re.sub(r'[^0-9]', '', text)) for text in filtered_texts]

        if filtered_texts:
            filtered_result = '\n'.join(filtered_texts)
        else:
            filtered_result = 'No text containing "k" found.'

        # 결과 출력
        print(f"Extracted Text:\n{processed_text}")
        print(f"Allowed Words:\n{allowed_texts}")
        print(f"Filtered Texts:\n{filtered_result}")
        print(f"Filtered Numbers:\n{filtered_numbers}")

        # 결과 반환
        return jsonify({
            "processed_text": processed_text,
            "allowed_texts": allowed_texts,
            "filtered_texts": filtered_result,
            "filtered_numbers": filtered_numbers
        })

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
